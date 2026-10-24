---
title: "Qt-QObject-Lebensdauer und QML-Kontext-Properties"
description: "Löschregeln auf Basis der Thread-Affinität und ein begrenzter Migrationsansatz für QML-Kontext-Properties in Qt 6."
tags: [cpp, qt, qml, qobject, lifetime]
level: 4
source_sha256: 91ed85c38fe743f8aa5b5543a899c1a4fc06190d8bf9432b561822236509ad4d
translation: machine
translated_at: '2026-10-24'
---
# Qt-QObject-Lebensdauer und QML-Kontext-Properties {#qt-qobject-lifetime-and-qml-context-properties}

Die Lebensdauer von Qt-6-Objekten wird durch QObject-Besitz, Thread-Affinität und den Zustand der Event-Loop bestimmt. Die Bereitstellung von QML-Kontexten fügt einen eigenen Lebensdauervertrag hinzu: Der Kontext besitzt ein injiziertes QObject nicht.

## Die Lebensdauer prüfen, nicht nur `deleteLater()` {#review-the-lifetime-not-just-deletelater}

Bevor ein Bereinigungspfad akzeptiert wird, sollten Sie den Besitzer des Objekts, seine aktuelle Affinität, die Frage, ob der besitzende Thread verzögerte Events verarbeiten kann, und das Ereignis bestimmen, das diesen Thread beendet.

| Situation | Korrektes Prüfergebnis |
| --- | --- |
| Parent und Child liegen in einem Thread | Das Parent besitzt das Child und löscht es. Parent und Child können nicht unterschiedliche Thread-Affinitäten haben. |
| Objekt empfängt gequeuete Arbeit | Dessen Event-Handler läuft im Thread seiner Affinität, nicht unbedingt im Thread des Aufrufers. |
| Ein anderer Thread benötigt Bereinigung | Direktes Löschen ist unsicher, außer Lebensdauer und Event-Verarbeitung sind synchronisiert. Bevorzugen Sie den dokumentierten Abbaupfad im Thread der Objekt-Affinität. |
| `deleteLater()` vor dem Start einer Event-Loop | Qt löscht das Objekt, nachdem diese Event-Loop gestartet wurde. |
| `deleteLater()` nach dem Stopp der Haupt-Event-Loop | Qt löscht das Objekt nicht. Das Herunterfahren erfordert eine frühere Bereinigungsentscheidung. |
| Objekt liegt in einem Worker-Thread ohne laufende Loop | Ein Objekt mit `deleteLater()` wird zerstört, wenn dieser Thread endet. |

Die allgemeine Regel „keine Event-Loop bedeutet keine Löschung“ ist falsch. Entscheidend ist die Lebenszyklusphase: Qt dokumentiert unterschiedliche Ergebnisse vor dem Start, nach dem Herunterfahren der Haupt-Loop und beim Beenden des Worker-Threads. [QObject](https://doc.qt.io/qt-6/qobject.html) und [Threads and QObjects](https://doc.qt.io/qt-6/threads-qobject.html) beschreiben diese Fälle.

### Abbau eines Worker-Objekts {#worker-object-teardown}

Halten Sie das QThread-Objekt und seinen Worker getrennt. Das QThread-Objekt hat die Affinität des Threads, der es erzeugt hat; es ist nicht der Worker-Thread selbst.

Das dokumentierte Worker-Objekt-Muster verbindet `QThread::finished()` mit `QObject::deleteLater()` des Workers. Dieses Muster ersetzt jedoch weder Abbruchlogik noch ein Abschlussprotokoll noch eine korrekte Reihenfolge: Fordern Sie den Abschluss über den eigenen Zustellungspfad des Workers an, lassen Sie den Thread enden und warten Sie, bevor Sie Objekte zerstören, die diesen Thread besitzen oder von ihm abhängen. Blockieren Sie den erzeugenden Thread nicht so, dass sein gequeueter Abschlusspfad nicht mehr ausgeführt werden kann.

## Die Bereitstellung von QML-Kontexten umfasst zwei getrennte Änderungen {#qml-context-exposure-has-two-separate-mutations}

`QQmlContext`-Properties sind Namen, die vom Kontext gehalten werden. Sie sind keine `QObject`-Properties. Das Hinzufügen oder Ersetzen eines solchen Namens mit `setContextProperty()` verändert den Kontext und kann erzwingen, dass Bindings in diesem Kontext neu ausgewertet werden, nachdem Objekte existieren.

Ein injiziertes Kontext-QObject unterscheidet sich davon. Seine `Q_PROPERTY`-Werte können über ihre `NOTIFY`-Signale geändert werden, ohne dass eine Kontext-Property hinzugefügt oder ersetzt wird. Behandeln Sie diese als getrennte Prüfungsfragen:

| Änderung | Prüfungsfrage |
| --- | --- |
| Kontextobjekt bzw. Kontext-Property hinzufügen, ersetzen oder ändern | War die gesamte Kontext-Einrichtung abgeschlossen, bevor die QML-Objekte erzeugt wurden? |
| Eine Property eines bestehenden injizierten QObjects aktualisieren | Hat die `Q_PROPERTY` das richtige `NOTIFY`-Signal, die richtige Thread-Affinität und die richtige Besitzerlebensdauer? |

`QQmlContext` legt fest, dass Eigenschaftsänderungen eines Kontextobjekts über das Notify-Signal der Property beobachtet werden, während das Setzen des Kontextobjekts oder das Hinzufügen von Kontext-Properties nach der Erzeugung eine Neuauswertung der Bindings erzwingt. [QQmlContext](https://doc.qt.io/qt-6/qqmlcontext.html) dokumentiert beide Verhaltensweisen.

### Begrenzte Kompatibilitätsbereitstellung {#bounded-compatibility-exposure}

Eine bestehende Bereitstellung von Kontext-Properties vor dem Laden kann eine Kompatibilitätsgrenze darstellen und muss nicht automatisch zu einer Umschreibung führen. Halten Sie sie begrenzt: Injizieren Sie vor `setSource()` oder der Komponentenerzeugung, dokumentieren Sie die Namen, die die QML-Wurzel erwartet, sorgen Sie dafür, dass der Besitzer des injizierten Objekts länger lebt als die QML-Engine, und verändern Sie die Form des Kontexts nach dem Start nicht mehr.

`setContextProperty()` überträgt den Besitz des injizierten QObjects nicht; dessen C++-Besitzer muss die QML-Nutzung überdauern. Für neue wiederverwendbare APIs sind Properties des Wurzelobjekts, registrierte Typen oder Singletons vorzuziehen. Kontext-Properties erzeugen nicht deklarierte Abhängigkeiten und sind für die Ahead-of-Time-Werkzeuge von QML unsichtbar. Siehe [Embedding C++ Objects into QML with Context Properties](https://doc.qt.io/qt-6/qtqml-cppintegration-contextproperties.html).

## Prüfliste {#review-checklist}

- Erfassen Sie Affinität und Besitzer jedes langlebigen QObjects, einschließlich seiner Kinder.
- Legen Sie für jede verzögerte Löschung fest, ob die betreffende Loop noch nicht gestartet wurde, läuft, gestoppt wurde oder mit einem Worker-Thread endet.
- Verfolgen Sie Abschluss, Abbruch, Thread-Ende und Zerstörung in dieser Reihenfolge; eine einzelne Verbindungszeile ist kein Abschaltprotokoll.
- Behandeln Sie jeden QML-Kontextnamen als implizite API-Abhängigkeit. Erfassen Sie Anbieter, Besitzer und den Zeitpunkt vor der QML-Objekterzeugung, zu dem er injiziert wird.
- Verwenden Sie für stabilen Live-Zustand eine QObject-Property mit `NOTIFY`; ersetzen Sie keinen Kontextnamen, um gewöhnliche Zustandsänderungen zu übermitteln.

## Fallstricke {#gotchas}

- **`deleteLater()` während des Herunterfahrens aufrufen:** Die Haupt-Event-Loop kann bereits gestoppt sein, sodass die verzögerte Löschung nie erfolgt. Legen Sie Besitz und Abbau fest, bevor die Loop endet.
- **Ein verschobenes QObject aus dem erzeugenden Thread löschen:** Die Affinität wandert mit dem QObject; ein threadübergreifendes direktes `delete` kann mit der Event-Zustellung konkurrieren. Verwenden Sie den Lebenszyklus des Workers und einen Löschpfad, der im Thread des Besitzers sicher ist.
- **Eine Kontext-Property für gewöhnliche Zustandsänderungen ersetzen:** Dadurch wird der Kontext verändert, und jedes Binding kann neu ausgewertet werden. Stellen Sie ein QObject mit `Q_PROPERTY` und `NOTIFY` bereit, wenn die Form stabil ist und sich nur Werte ändern.
- **Annehmen, QML besitze einen injizierten Zeiger:** `QQmlContext` übernimmt keinen Besitz. Ein Stack-Objekt ist nur gültig, solange sein C++-Gültigkeitsbereich die View oder Engine überdauert, die es verwendet.
- **Kontextinjektion als unsichtbaren, harmlosen Klebstoff behandeln:** Die QML-Datei hat eine nicht deklarierte Abhängigkeit, die `qmllint`, der QML-Language-Server und der Quick Compiler nicht im Voraus auflösen können.

## Einschränkungen {#limitations}

Dies ist eine Prüfreferenz, kein Laufzeitnachweis für eine konkrete Anwendung. Sie legt weder das Abbruchprotokoll, die QML-Modulgrenze noch die Reihenfolge des Herunterfahrens einer Anwendung fest. Überprüfen Sie den tatsächlichen Affinitätsgraphen, die Signalverbindungen, den Besitz der Event-Loop sowie das Verhalten beim Start und Herunterfahren im Zielbuild.

## Siehe auch {#see-also}

- [[object-lifetime]]
- [[scope-and-lifetime]]
- [[concurrency]]
- [[smart-pointers]]
