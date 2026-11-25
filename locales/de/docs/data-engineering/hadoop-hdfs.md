---
title: "Hadoop und HDFS"
category: tools
tags: [data-engineering, hadoop, hdfs, distributed-storage, big-data]
level: 4
source_sha256: 09548d32acaf410387f7bbee7e5e0f758b3329875c366ac623633336e92e9cd4
translation: machine
translated_at: '2026-10-24'
---
# Hadoop und HDFS {#hadoop-and-hdfs}

Hadoop ist ein Framework für die verteilte Speicherung und Verarbeitung großer Datenmengen. HDFS (Hadoop Distributed File System) bietet fehlertolerante Speicherung auf handelsüblicher Hardware.

## Hadoop-Architektur {#hadoop-architecture}

```bash
Application Layer: MapReduce | Spark | Tez | Hive | Pig
Resource Layer:    YARN (Resource Management)
Storage Layer:     HDFS (Distributed File System)
```

**Ökosystem-Werkzeuge:** Ambari (Verwaltungs-UI), ZooKeeper (Koordination), Sqoop/Flume (Ingestion), Oozie (Scheduling), HBase (NoSQL), Mahout (ML).

## HDFS-Architektur {#hdfs-architecture}

```javascript
Client -> NameNode (Active) -- Standby NameNode (HA)
              |                 Secondary NameNode (checkpoints)
    +---------+---------+
    DN1     DN2     DN3     (DataNodes)
```

| Komponente | Rolle |
|-----------|------|
| **NameNode** | Speichert Metadaten – Dateispeicherorte, Blockspeicherorte, Berechtigungen. Speichert KEINE Daten |
| **DataNode** | Speichert Datenblöcke auf der lokalen Festplatte |
| **Secondary NameNode** | Führt Edit-Logs mit dem Checkpoint zusammen. KEIN Failover |
| **Standby NameNode** | HA-Failover für den aktiven NameNode |

**Kritisch:** Gehen alle NameNodes verloren, werden die HDFS-Daten nicht mehr zugänglich (Metadaten sind weg).

## Blockspeicherung {#block-storage}

- Standard-Blockgröße: **128 MB** (pro Datei konfigurierbar)
- Standard-Replikationsfaktor: **3** (jeder Block auf 3 DataNodes)
- Plattenbedarf: Eine 2-GB-Datei mit Replikationsfaktor 3 belegt **6 GB** physisch
- **Rack-Awareness:** Zur Ausfallsicherheit auf unterschiedliche Racks replizieren

## HDFS-Eigenschaften {#hdfs-properties}

| Eigenschaft | Detail |
|----------|--------|
| Nur anhängbar (Append-only) | Dateien können nach dem Schreiben nicht mehr geändert werden |
| Optimiert für Durchsatz | Auf Kosten der Latenz |
| Nicht POSIX-konform | Andere Semantik als ein lokales Dateisystem |
| Pro Datei konfigurierbar | Blockgröße und Replikationsfaktor |

## Problem kleiner Dateien {#small-files-problem}

10 Mio. Dateien mit insgesamt 1 GB: Jede Datei = 1 Block. Der NameNode speichert ca. 150 Bytes Metadaten pro Block. 10 Mio. * 150 Bytes = ca. 1,5 GB Metadaten > tatsächliche Daten.

**Lösungen:** In größere Dateien zusammenfassen (SequenceFiles, HAR-Archive).

## HDFS-Befehle {#hdfs-commands}

```bash
hadoop fs -ls /path                # list files
hadoop fs -put local.txt /hdfs/    # upload
hadoop fs -get /hdfs/file.txt ./   # download
hadoop fs -cat /hdfs/file.txt      # view content
hadoop fs -text /hdfs/file.txt     # view (handles compression)
hadoop fs -mkdir /hdfs/dir         # create directory
hadoop fs -rm -r /hdfs/output/     # delete recursively
hdfs dfsadmin -report              # cluster health
hdfs fsck file -files -blocks -locations  # check blocks

# Custom block size and replication
hadoop fs -D dfs.blocksize=67108864 -D dfs.replication=2 -put file.txt /hdfs/
```

## DataNode-Heartbeats {#datanode-heartbeats}
- DataNodes senden periodisch Heartbeats AN den NameNode (nicht umgekehrt)
- Ausbleibende Heartbeats lösen eine Prüfung durch den NameNode und anschließende Re-Replikation aus
- DataNode kennt seine Blöcke und Prüfsummen, aber NICHT die Dateien, zu denen sie gehören

## Prinzip der Datenlokalität {#data-locality-principle}
Berechnung zu den Daten bringen, nicht Daten zur Berechnung. Vermeidet den Netzwerkengpass. Deshalb dominieren funktionale Muster (map, reduce, filter) im Big-Data-Umfeld.

## Big Data 5V {#big-data-5v}

| V | Bedeutung |
|---|---------|
| **Volume** | Datenmenge (TB, PB) |
| **Velocity** | Anforderung an die Verarbeitungsgeschwindigkeit |
| **Value** | Geschäftliche Bedeutung |
| **Veracity** | Vertrauenswürdigkeit der Daten |
| **Variety** | Vielfalt der Datentypen |

## Stolperfallen {#gotchas}
- HDFS-Splits != HDFS-Blöcke: Splits sind logisch (MapReduce), Blöcke sind physisch
- Kleine Dateien sind problematisch – Speicherlast im NameNode
- `hadoop distcp` für das Kopieren von S3 nach HDFS (verteiltes Kopieren über MR)
- S3 ist 5–10× günstiger als HDFS und praktisch unbegrenzt

## Siehe auch {#see-also}
- [[mapreduce]] - Verarbeitungsparadigma
- [[yarn-resource-management]] - Verwaltung der Cluster-Ressourcen
- [[apache-hive]] - SQL auf Hadoop
- [[hbase]] - NoSQL auf HDFS
- [[file-formats]] - Parquet, ORC, Avro
