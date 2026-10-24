---
title: "Группы консьюмеров"
category: concepts
tags: [kafka, consumer, group, rebalancing, heartbeat, partition-assignment, static-membership]
level: 4
source_sha256: a8b274145e723ce1bf8ce34e4c90f32fce90e9979643464bea0ca8f01b0c80e8
translation: machine
translated_at: '2026-10-24'
---
# Группы консьюмеров {#consumer-groups}

Группа консьюмеров — это именованная сущность, которая позволяет нескольким консьюмерам совместно читать партиции топиков. Каждая партиция назначается ровно одному консьюмеру в группе, что обеспечивает и параллелизм, и отказоустойчивость.

## Ключевые факты {#key-facts}

- Консьюмеры присоединяются к группе через параметр `group.id`, который должен быть уникальным для каждой логической группы консьюмеров
- В пределах группы **одну партицию может читать только один консьюмер** (но один консьюмер может читать несколько партиций)
- Если консьюмеров больше, чем партиций, лишние консьюмеры простаивают (работы для них нет)
- Несколько групп консьюмеров МОГУТ независимо читать одну и ту же партицию (каждая группа хранит собственные [[offsets-and-commits]])
- Это ключевое преимущество: чтение топика 10 раз требует 10 групп консьюмеров (10 x 8 байт на партицию), а не 10 копий данных
- Один консьюмер может подписаться на несколько топиков через `consumer.subscribe(List<String>)`
- Жёсткого ограничения на количество групп консьюмеров нет (теоретически около 2 миллиардов); топик `__consumer_offsets` (по умолчанию 50 партиций) начинает тормозить при тысячах групп
- Первый консьюмер, подключившийся к группе, становится **лидером группы**: он выполняет перераспределение партиций при ребалансировке
- Таймаут группы консьюмеров: если консьюмер неактивен слишком долго, Kafka может удалить его смещения (`offsets.retention.minutes`, по умолчанию 7 дней)
- Kafka работает по **pull-модели**: консьюмеры опрашивают Kafka, а Kafka не выталкивает сообщения (в отличие от RabbitMQ)

## Шаблоны {#patterns}

### Базовый консьюмер (Java) {#basic-consumer-java}

```java
Properties props = new Properties();
props.put("bootstrap.servers", "localhost:9092");
props.put("group.id", "my-group");
props.put("key.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
props.put("value.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
props.put("enable.auto.commit", "false");
props.put("auto.offset.reset", "earliest");

KafkaConsumer<String, String> consumer = new KafkaConsumer<>(props);
consumer.subscribe(Arrays.asList("topic1", "topic2"));

try {
    while (true) {
        ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
        for (ConsumerRecord<String, String> record : records) {
            processRecord(record);
        }
        consumer.commitSync();
    }
} finally {
    consumer.close();  // ALWAYS close consumer
}
```

### Базовый консьюмер (Python) {#basic-consumer-python}

```python
from confluent_kafka import Consumer

conf = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "my-group",
    "auto.offset.reset": "earliest",
    "enable.auto.commit": False,
}
consumer = Consumer(conf)
consumer.subscribe(["topic1", "topic2"])

try:
    while True:
        msg = consumer.poll(0.1)
        if msg is None:
            continue
        if msg.error():
            print(f"Error: {msg.error()}")
            continue
        process_message(msg)
        consumer.commit(msg)
finally:
    consumer.close()
```

### Стратегии назначения партиций {#partition-assignment-strategies}

| Стратегия | Сценарий использования | Поведение |
|----------|----------|----------|
| **RangeAssignor** (по умолчанию) | Ко-партиционированные топики | Назначает непрерывные партиции для каждого топика; может быть несбалансированной |
| **RoundRobinAssignor** | Справедливое распределение | Распределяет все партиции равномерно, поочерёдно |
| **StickyAssignor** | Стateful-консьюмеры | Сохраняет существующие назначения при ребалансировке |
| **CooperativeStickyAssignor** | Современное значение по умолчанию (рекомендуется) | Инкрементальная ребалансировка без stop-the-world |

```java
props.put("partition.assignment.strategy",
    "org.apache.kafka.clients.consumer.CooperativeStickyAssignor");
```

**Ко-партиционированные топики**: два топика с одинаковым количеством партиций, одинаковой стратегией партиционирования и одинаковыми ключами. При использовании RangeAssignor данные с одинаковым ключом из обоих топиков попадают к одному и тому же консьюмеру, что позволяет выполнять соединения (join) без межпроцессного взаимодействия.

### Справочник параметров консьюмера {#consumer-configuration-reference}

| Параметр | По умолчанию | Описание |
|-----------|---------|-------------|
| `bootstrap.servers` | обязателен | Адреса брокеров (через запятую) |
| `group.id` | обязателен | Идентификатор группы консьюмеров |
| `key.deserializer` | обязателен | Класс десериализации ключей |
| `value.deserializer` | обязателен | Класс десериализации значений |
| `enable.auto.commit` | `true` | Автоматическая фиксация смещений (в продакшене лучше отключить) |
| `auto.commit.interval.ms` | `5000` | Частота автоматической фиксации |
| `auto.offset.reset` | `latest` | Что делать, если сохранённого смещения нет |
| `max.partition.fetch.bytes` | `1048576` (1 МБ) | Максимум данных на партицию за один poll |
| `max.poll.records` | `500` | Максимум сообщений за один poll по всем партициям |
| `fetch.min.bytes` | `1` | Минимум данных, при котором poll возвращает результат |
| `fetch.max.wait.ms` | `500` | Максимальное ожидание, если `fetch.min.bytes` не набран |
| `heartbeat.interval.ms` | `3000` | Частота heartbeat |
| `session.timeout.ms` | `10000` | Таймаут сессии, после которого консьюмер считается мёртвым |
| `max.poll.interval.ms` | `300000` | Максимальное время между poll |

### Статическое членство в группе {#static-group-membership}

```java
props.put("group.instance.id", "consumer-instance-1");
// No rebalance on temporary disconnect
// Risk: partition unread until restart
```

## Подводные камни {#gotchas}

- **Шторм ребалансировок** — консьюмеры многократно останавливаются и возобновляют чтение; причины: обработка занимает дольше, чем `session.timeout.ms`, медленный запуск, частые деплои; решение: увеличить таймауты, использовать CooperativeStickyAssignor
- **Все консьюмеры должны использовать одну и ту же стратегию назначения** — несовпадение приводит к глобальной ребалансировке
- **Приостановленные консьюмеры НЕ запускают ребалансировку** — вызов `.pause()` поддерживает heartbeat
- **Подписка консьюмера фиксируется для каждого вызова subscribe** — повторный вызов `subscribe()` заменяет предыдущую подписку
- **Лишние консьюмеры простаивают** — консьюмеров больше, чем партиций, означает растрату ресурсов; заранее планируйте количество партиций (эмпирическое правило: 4 партиции на консьюмера)

## См. также {#see-also}

- [[offsets-and-commits]] — отслеживание смещений, опасности автоматической фиксации, шаблоны ручной фиксации
- [[rebalancing-deep-dive]] — настройка heartbeat, кооперативная ребалансировка, статическое членство
- [[topics-and-partitions]] — выбор количества партиций и маршрутизация по ключу
- [[consumer-configuration]] — полный справочник параметров консьюмера
- [Apache Kafka Consumer Configuration](https://kafka.apache.org/documentation/#consumerconfigs)
