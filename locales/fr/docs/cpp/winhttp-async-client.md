---
title: "Client asynchrone WinHTTP"
description: "Notifications de fin contre notifications de progression, attentes bornées et sémantique de l'annulation pour WinHTTP en mode WINHTTP_FLAG_ASYNC. Pourquoi un client asynchrone reste bloqué indéfiniment et comment prouver lequel des trois défauts vous avez."
level: 4
source_sha256: a19669f19678837aebd796ac935a3e0ceb304511e3d52d7b4c173bf6db006496
translation: machine
translated_at: '2026-10-24'
---
# Client asynchrone WinHTTP {#winhttp-asynchronous-client}

Un client WinHTTP asynchrone qui « reste bloqué » présente presque toujours l'un de trois défauts indépendants : il ne s'est jamais abonné à la notification de fin qu'il attend, il attend sans borne, ou il annule sa propre requête saine. Chacun a une signature distincte et peut être prouvé isolément. Vérifié avec `winhttp.h` du Windows SDK 10.0.26100.0 et la documentation officielle actuelle.

## Modèle de notification : progression n'est pas achèvement {#notification-model-progress-is-not-completion}

`WinHttpSetStatusCallback` prend un masque de bits `dwNotificationFlags`. Ce sont les noms qui piègent : plusieurs indicateurs semblent couvrir l'achèvement, alors qu'ils ne développent qu'en notifications de *progression*. D'après l'en-tête du SDK :

```c
/* progress only - fires while the header is going out */
#define WINHTTP_CALLBACK_FLAG_SEND_REQUEST \
    (WINHTTP_CALLBACK_STATUS_SENDING_REQUEST | WINHTTP_CALLBACK_STATUS_REQUEST_SENT)

#define WINHTTP_CALLBACK_FLAG_RECEIVE_RESPONSE \
    (WINHTTP_CALLBACK_STATUS_RECEIVING_RESPONSE | WINHTTP_CALLBACK_STATUS_RESPONSE_RECEIVED)

/* the actual completions */
#define WINHTTP_CALLBACK_FLAG_SENDREQUEST_COMPLETE  WINHTTP_CALLBACK_STATUS_SENDREQUEST_COMPLETE
#define WINHTTP_CALLBACK_FLAG_READ_COMPLETE         WINHTTP_CALLBACK_STATUS_READ_COMPLETE
#define WINHTTP_CALLBACK_FLAG_WRITE_COMPLETE        WINHTTP_CALLBACK_STATUS_WRITE_COMPLETE
#define WINHTTP_CALLBACK_FLAG_REQUEST_ERROR         WINHTTP_CALLBACK_STATUS_REQUEST_ERROR

#define WINHTTP_CALLBACK_FLAG_HANDLES \
    (WINHTTP_CALLBACK_STATUS_HANDLE_CREATED | WINHTTP_CALLBACK_STATUS_HANDLE_CLOSING)
```

Il existe exactement six notifications d'achèvement, et chacune correspond à l'appel qu'elle termine :

| Notification d'achèvement | Termine |
|---|---|
| `WINHTTP_CALLBACK_STATUS_SENDREQUEST_COMPLETE` | `WinHttpSendRequest` |
| `WINHTTP_CALLBACK_STATUS_HEADERS_AVAILABLE` | `WinHttpReceiveResponse` |
| `WINHTTP_CALLBACK_STATUS_DATA_AVAILABLE` | `WinHttpQueryDataAvailable` |
| `WINHTTP_CALLBACK_STATUS_READ_COMPLETE` | `WinHttpReadData` |
| `WINHTTP_CALLBACK_STATUS_WRITE_COMPLETE` | `WinHttpWriteData` |
| `WINHTTP_CALLBACK_STATUS_REQUEST_ERROR` | l'un des précédents, en cas d'échec |

`WINHTTP_CALLBACK_STATUS_REQUEST_ERROR` est la seule notification d'achèvement qui signifie un échec ; toutes les autres signifient que l'appel correspondant a réussi.

**Signature mesurée d'un mauvais abonnement :** un client abonné avec `SEND_REQUEST | RECEIVE_RESPONSE` journalisait normalement les notifications de progression, mais recevait **0 achèvement en 120 000 ms**. Le même client, avec les indicateurs d'achèvement ajoutés, a terminé la même requête en **78 ms**. Les notifications de progression continuent d'arriver, donc le journal paraît vivant, ce qui explique que ce défaut échappe à une inspection superficielle.

### Abonnement correct {#correct-subscription}

```cpp
// Subscribe to every completion plus handle lifetime. ALL_COMPLETIONS covers the six
// completions above; HANDLES adds HANDLE_CREATED / HANDLE_CLOSING for context lifetime.
const DWORD kFlags = WINHTTP_CALLBACK_FLAG_ALL_COMPLETIONS
                   | WINHTTP_CALLBACK_FLAG_HANDLES;

if (WinHttpSetStatusCallback(hSession, &OnWinHttpStatus, kFlags, 0)
        == WINHTTP_INVALID_STATUS_CALLBACK) {
    return HRESULT_FROM_WIN32(GetLastError());
}
```

Utilisez `WINHTTP_CALLBACK_FLAG_ALL_NOTIFICATIONS` (0xffffffff) pendant le débogage : WinHTTP est verbeux sur sa propre machine à états, et la trace supplémentaire se révèle utile. Restreignez-le ensuite.

`WinHttpSetStatusCallback` est lui-même synchrone même sous `WINHTTP_FLAG_ASYNC` ; sa valeur de retour fait foi. Le callback défini sur un handle de session est hérité par les handles de requête créés à partir de lui, mais le modifier ensuite ne se propage pas aux handles déjà dérivés : définissez-le à chaque niveau qui vous importe.

### Lier abonnement et traitement à la compilation {#bind-subscription-to-handling-at-compile-time}

La classe de défaut est « le switch traite une notification à laquelle personne ne s'est abonné » (branche morte) ou « l'abonnement inclut une notification que personne ne traite » (perte silencieuse). Ce sont des faits statiques : vérifiez-les statiquement :

```cpp
constexpr DWORD kSubscribed = WINHTTP_CALLBACK_FLAG_ALL_COMPLETIONS
                            | WINHTTP_CALLBACK_FLAG_HANDLES;

// Every notification the dispatcher has a case for must be subscribed.
static_assert(kSubscribed & WINHTTP_CALLBACK_STATUS_SENDREQUEST_COMPLETE, "no send completion");
static_assert(kSubscribed & WINHTTP_CALLBACK_STATUS_HEADERS_AVAILABLE,   "no headers completion");
static_assert(kSubscribed & WINHTTP_CALLBACK_STATUS_DATA_AVAILABLE,      "no data completion");
static_assert(kSubscribed & WINHTTP_CALLBACK_STATUS_READ_COMPLETE,       "no read completion");
static_assert(kSubscribed & WINHTTP_CALLBACK_STATUS_REQUEST_ERROR,       "no error completion");
static_assert(kSubscribed & WINHTTP_CALLBACK_STATUS_HANDLE_CLOSING,      "no closing notice");
```

C'est la garde la moins coûteuse possible : elle ne coûte rien à l'exécution et fait échouer la compilation dès que quelqu'un « nettoie » la liste des indicateurs.

## Attendre avec une borne {#waiting-with-a-bound}

Une notification d'achèvement qui n'arrive jamais doit tout de même mettre fin à l'opération. `INFINITE` transforme un bug d'abonnement, une connexion coupée ou un proxy bloqué en thread impossible à arrêter.

```cpp
// Bounded wait. Distinguish the three outcomes; never collapse timeout into failure.
enum class WaitResult { Completed, TimedOut, Abandoned };

WaitResult WaitForCompletion(HANDLE hEvent, DWORD timeoutMs) {
    const DWORD rc = WaitForSingleObject(hEvent, timeoutMs);  // never INFINITE
    switch (rc) {
        case WAIT_OBJECT_0: return WaitResult::Completed;
        case WAIT_TIMEOUT:  return WaitResult::TimedOut;
        default:            return WaitResult::Abandoned;     // WAIT_ABANDONED / WAIT_FAILED
    }
}
```

Le délai d'attente est un troisième état, ni un échec ni un succès : la même discipline à trois états qui s'applique à toute vérification de santé. Voir [[three-state-check-aggregation]].

## Annulation : fermer le handle, c'est annuler {#cancellation-closing-the-handle-is-the-cancel}

Il n'existe pas de `WinHttpCancel`. Une requête asynchrone en cours s'annule en fermant son handle de requête, et les règles qui l'entourent sont impitoyables :

- Après `WinHttpCloseHandle`, le handle ne doit plus jamais être passé à une fonction WinHTTP, depuis aucun thread, y compris `WinHttpCloseHandle` lui-même. WinHTTP réutilise les valeurs de handle, donc une double fermeture peut toucher la requête de quelqu'un d'autre.
- Des callbacks peuvent encore arriver après le retour de la fermeture ; WinHTTP démonte les handles de manière asynchrone. Une opération annulée se manifeste par `WINHTTP_CALLBACK_STATUS_REQUEST_ERROR`.
- Fermer un handle **parent** (session, connexion) n'annule pas une opération en attente sur un handle de requête **enfant**. Annulez le handle qui possède l'opération.
- Même lorsque le handle est fermé, l'opération peut encore se terminer avec succès plutôt que d'être annulée. Les deux issues sont légales ; gérez les deux.
- Gardez l'objet de contexte vivant jusqu'à l'arrivée de `WINHTTP_CALLBACK_STATUS_HANDLE_CLOSING`. Mettre le callback à `NULL` ne rend pas cela sûr : WinHTTP ne synchronise pas `WinHttpSetStatusCallback` avec les callbacks déjà en cours sur les threads de travail.

**Signature mesurée d'une auto-annulation :** un appel de fermeture de nouvelle tentative placé dans la boucle d'attente s'est déclenché au premier tick de 50 ms et a fermé une requête parfaitement saine. La panne s'est manifestée par `ERROR_WINHTTP_OPERATION_CANCELLED` (12017) signalée sur `WinHttpSendRequest`, un appel qui avait déjà été émis avec succès. 12017 signifie « le handle sur lequel opérait la requête a été fermé avant la fin de l'opération » ; lorsqu'il apparaît sans annulation externe, l'appelant a fermé son propre handle.

```cpp
// Close exactly once, from one place, and only when a cancel is actually intended.
std::atomic<bool> closed{false};
if (!closed.exchange(true)) {
    WinHttpCloseHandle(hRequest);   // the only close for this handle
}
// Do NOT put a close/retry-close inside the poll loop that is waiting for the completion.
```

## Règles de tampons et de threads qui mordent plus tard {#buffer-and-thread-rules-that-bite-later}

- WinHTTP ne copie pas vos tampons. Un tampon d'envoi doit rester valide de `WinHttpSendRequest` jusqu'à `SENDREQUEST_COMPLETE` ; un tampon de réception, de `WinHttpReadData` jusqu'à `READ_COMPLETE`. Des tampons sur la pile d'une fonction qui retourne avant l'achèvement constituent une utilisation après libération déclenchée par le timing réseau. Voir [[object-lifetime]] et [[raii-resource-management]].
- Utilisez un tampon de réception d'au moins 8 Ko. De petits tampons poussent le cycle `WinHttpQueryDataAvailable` / `WinHttpReadData` vers une récursion profonde et peuvent épuiser la pile.
- WinHTTP délivre les notifications sur un seul thread pour tout le processus. Bloquer dans un callback fige toutes les requêtes HTTP du processus et fait croître la mémoire en mode noyau. Copiez ce dont vous avez besoin, signalez, puis retournez.
- Le callback s'exécute sur un thread différent de celui qui a émis l'appel, et il peut être réentré pour une autre requête. Il doit être thread-safe. La seule exception est `HANDLE_CLOSING`, garantie comme dernière notification pour ce handle.
- Une notification peut arriver **avant** que la valeur de contexte ne soit définie, car le contexte n'est fourni que par `WinHttpSendRequest` / `WinHttpSetOption`. Gérez `dwContext == NULL`.

## Diagnostiquer lequel des défauts vous avez {#diagnosing-which-defect-you-have}

Exécutez le client une fois avec une trace complète des notifications et comptez ce qui arrive :

```cpp
void CALLBACK OnWinHttpStatus(HINTERNET, DWORD_PTR ctx, DWORD status,
                              LPVOID info, DWORD infoLen) {
    // Trace every notification id; completions are the six ids listed above.
    Trace("winhttp status=0x%08X ctx=%p len=%u", status, (void*)ctx, infoLen);
    if (status == WINHTTP_CALLBACK_STATUS_REQUEST_ERROR && info) {
        auto* r = static_cast<WINHTTP_ASYNC_RESULT*>(info);
        Trace("  request_error api=%lu code=%lu", r->dwResult, r->dwError);
    }
}
```

| Observation | Défaut |
|---|---|
| Les notifications de progression circulent, zéro achèvement, l'attente ne retourne jamais | Indicateurs d'achèvement non abonnés |
| L'achèvement apparaît dans la trace mais l'appelant reste bloqué | Attente non liée à cette notification, ou `INFINITE` sur le mauvais objet |
| `REQUEST_ERROR` avec `dwError == 12017` et sans annulation externe | Le client a fermé son propre handle |
| Rien du tout, pas même `HANDLE_CREATED` | Callback jamais installé, ou installé sur le mauvais niveau de handle |

## Pièges {#gotchas}

- **Problème :** `WINHTTP_CALLBACK_FLAG_SEND_REQUEST` se lit comme « l'envoi de la requête est terminé », et la formulation de la documentation « début et fin de l'envoi d'un en-tête de requête » le renforce. Il se développe en `SENDING_REQUEST | REQUEST_SENT` : deux notifications de progression, aucun bit d'achèvement. -> **Correction :** abonnez-vous à `WINHTTP_CALLBACK_FLAG_ALL_COMPLETIONS` (ou aux indicateurs d'achèvement explicites plus `REQUEST_ERROR`) et verrouillez-le avec `static_assert`.
- **Problème :** un chemin de nouvelle tentative ou de nettoyage appelle `WinHttpCloseHandle` depuis la boucle qui attend l'achèvement ; le premier tick tue la requête en cours, et le symptôme est un 12017 attribué à un appel déjà réussi. -> **Correction :** fermez depuis un seul endroit, protégé par un drapeau atomique, et jamais sur un minuteur qui s'exécute en parallèle de l'attente.
- **Problème :** `WaitForSingleObject(hEvent, INFINITE)` transforme toute notification manquante en blocage permanent sans diagnostic. -> **Correction :** passez toujours un délai fini et traitez le délai d'attente comme une issue à part entière, distincte du succès et de l'échec.
- **Problème :** contexte ou tampon libéré après le retour de `WinHttpCloseHandle`, en supposant que le handle est mort. Des callbacks peuvent encore être en vol sur un thread de travail. -> **Correction :** ne libérez qu'après `WINHTTP_CALLBACK_STATUS_HANDLE_CLOSING`, ce qui exige de s'abonner à `WINHTTP_CALLBACK_FLAG_HANDLES`.
- **Problème :** annuler en fermant le handle de session pendant qu'une requête est en attente. L'opération enfant n'est pas annulée et le code poursuit comme si elle l'était. -> **Correction :** fermez le handle de requête qui possède l'opération.
- **Problème :** le callback effectue un vrai travail (analyse, E/S disque, journalisation vers un puits lent), si bien que toutes les requêtes HTTP du processus ralentissent ou se bloquent ensemble. -> **Correction :** le callback copie l'état et signale ; le travail se fait sur le thread de l'appelant.

## Voir aussi {#see-also}

- [Gestion des erreurs - Exceptions et alternatives](error-handling.md) - propagation des erreurs à travers une frontière d'API C
- [[object-lifetime]] - règles de durée de vie des tampons et des contextes
- [[raii-resource-management]] - wrappers de handles à propriétaire unique
- [Concurrence - Threads, asynchrone, atomiques](concurrency.md) - exigences de thread-safety pour les callbacks
- [[external-heartbeat-monitoring-for-native-process-crashes]] - détecter le blocage depuis l'extérieur
- [[three-state-check-aggregation]] - le délai d'attente comme verdict distinct
- [WinHttpSetStatusCallback](https://learn.microsoft.com/windows/win32/api/winhttp/nf-winhttp-winhttpsetstatuscallback)
- [WINHTTP_STATUS_CALLBACK](https://learn.microsoft.com/windows/win32/api/winhttp/nc-winhttp-winhttp_status_callback)
- [WinHttpCloseHandle](https://learn.microsoft.com/windows/win32/api/winhttp/nf-winhttp-winhttpclosehandle)
- [Concurrence dans WinHTTP](https://learn.microsoft.com/windows/win32/winhttp/concurrency-in-winhttp)
- [Messages d'erreur WinHTTP](https://learn.microsoft.com/windows/win32/winhttp/error-messages)
