---
title: "Zeitreihenanalyse"
category: techniques
tags: [data-science, time-series, forecasting, arima, seasonality, varma, garch, prophet]
level: 3
source_sha256: 255decfbb7abc0eddeb82ad6786b5c79cb5d7d1b0e4b8a3482e263d3171eda38
translation: machine
translated_at: '2026-10-24'
---
# Zeitreihenanalyse {#time-series-analysis}

Nach Zeit geordnete Daten. Sie erfordern eine besondere Behandlung, da die Beobachtungen NICHT unabhängig voneinander sind. Zeitliche Muster (Trend, Saisonalität, Autokorrelation) müssen explizit modelliert werden.

## Komponenten einer Zeitreihe {#components-of-time-series}

- **Trend**: langfristige Richtung (aufwärts, abwärts, konstant)
- **Saisonalität**: sich wiederholende Muster in festen Intervallen (täglich, wöchentlich, jährlich)
- **Zyklisch**: sich wiederholende Muster in nicht festen Intervallen (Konjunkturzyklen)
- **Residuum/Rauschen**: zufällige Schwankungen nach Entfernung von Trend und Saisonalität

## Stationarität {#stationarity}

Eine Zeitreihe ist stationär, wenn sich ihre statistischen Eigenschaften (Mittelwert, Varianz) über die Zeit nicht ändern. Die meisten Modelle setzen Stationarität voraus.

**Tests:**
- **ADF-Test** (Augmented Dickey-Fuller): p < 0,05 -> stationär
- Visuell: Diagramm erstellen und auf konstanten Mittelwert/konstante Varianz prüfen

**Stationär machen:**
- **Differenzbildung**: y_diff = y_t - y_(t-1). Entfernt einen linearen Trend
- **Log-Transformation**: stabilisiert die Varianz
- **Saisonale Differenzbildung**: y_t - y_(t-Periode)

## Klassische Modelle {#classical-models}

### AR (AutoRegressive) {#ar-autoregressive}
y_t = c + phi_1 * y_(t-1) + ... + phi_p * y_(t-p) + Fehler

Vorhersage aus vergangenen Werten. Ordnung p = Anzahl der Lags.

### MA (Moving Average) {#ma-moving-average}
y_t = c + theta_1 * e_(t-1) + ... + theta_q * e_(t-q) + Fehler

Vorhersage aus vergangenen Fehlern. Ordnung q = Anzahl der Fehler-Lags.

### ARMA / ARIMA {#arma-arima}
- **ARMA(p,q)**: AR und MA kombiniert (setzt Stationarität voraus)
- **ARIMA(p,d,q)**: d = Ordnung der Differenzbildung. Verarbeitet nicht stationäre Daten
- **SARIMA(p,d,q)(P,D,Q,s)**: plus saisonale Komponente mit Periode s

```python
from statsmodels.tsa.arima.model import ARIMA

model = ARIMA(y_train, order=(2, 1, 1))  # AR=2, diff=1, MA=1
results = model.fit()
forecast = results.forecast(steps=30)
```

### Exponentielle Glättung {#exponential-smoothing}

Gewichteter Mittelwert vergangener Beobachtungen mit exponentiell abnehmenden Gewichten.

**SES** (Simple Exponential Smoothing): kein Trend, keine Saisonalität. Entspricht EWMA (exponentially weighted moving average). Ein einziger Glättungsparameter alpha steuert die Abklingrate.

```python
from statsmodels.tsa.holtwinters import ExponentialSmoothing, SimpleExpSmoothing

# Simple Exponential Smoothing
ses_model = SimpleExpSmoothing(y_train).fit(smoothing_level=0.2)
forecast_ses = ses_model.forecast(12)

# Holt-Winters (trend + seasonality)
model = ExponentialSmoothing(y_train, trend='add', seasonal='mul', seasonal_periods=12)
results = model.fit()
forecast = results.forecast(12)
```

**Varianten**: SES (nur Niveau) -> Holt (+ Trend) -> Holt-Winters (+ Saisonalität). Verwenden Sie `seasonal='add'` für konstante saisonale Amplitude und `seasonal='mul'`, wenn die Amplitude mit dem Niveau wächst.

### VAR / VARMA (multivariat) {#var-varma-multivariate}

Vektorautoregressive Modelle: Mehrere korrelierte Zeitreihen werden gemeinsam vorhergesagt. Jede Reihe hängt von ihren eigenen Lags UND den Lags aller anderen Reihen ab.

- Die Parameter sind **Matrizen** (D x D) statt Skalare, wobei D = Anzahl der Zeitreihen
- **VAR(p)**: rein autoregressiv, am häufigsten verwendet (die Schätzung von VARMA ist numerisch instabil)
- **VARMA(p,q)**: vektorielles ARMA, ergänzt um eine Komponente gleitender Durchschnitte
- Datenformat: T Zeilen x D Spalten (T Zeitschritte, D Reihen)

```python
from statsmodels.tsa.statespace.varmax import VARMAX
from statsmodels.tsa.api import VAR

# VAR model (recommended - simpler, more stable)
var_model = VAR(train_df[['series_1', 'series_2']])
results = var_model.fit(maxlags=4)
forecast = results.forecast(train_df[['series_1', 'series_2']].values[-4:], steps=12)

# VARMAX (supports exogenous variables)
model = VARMAX(train_scaled, order=(2, 1))
results = model.fit(disp=False, maxiter=500)
forecast = results.forecast(steps=n_test)
```

**Praktische Hinweise**: Skalieren Sie multivariate Reihen immer vor dem Anpassen (unterschiedliche Einheiten/Größenordnungen). ACF/PACF pro Reihe dienen als grobe Orientierung, aber die Kreuzterme sind relevant. Die praktikable Methode ist eine Rastersuche über (p,q). Ökonometrische Datensätze (BIP, Zinssätze, Zinsspannen) sind der klassische Anwendungsfall für VARMA.

### GARCH (Volatilitätsmodellierung) {#garch-volatility-modeling}

GARCH modelliert zeitveränderliche Varianz (Volatilitätscluster). Unverzichtbar für Finanzzeitreihen, deren Varianz nicht konstant ist.

- **ARCH(q)**: Varianz hängt von vergangenen quadrierten Fehlern ab
- **GARCH(p,q)**: Varianz hängt von vergangenen quadrierten Fehlern UND vergangenen Varianzen ab
- Das Standard-GARCH(1,1) ist das Arbeitspferd unter den Modellen

```python
from arch import arch_model

# Scale returns first - GARCH needs values between 1 and 1000
m, s = train_returns.mean(), train_returns.std()
train_scaled = (train_returns - m) / s

# GARCH(1,1)
model = arch_model(train_scaled, vol='GARCH', p=1, q=1)
result = model.fit(update_freq=5)
print(result.summary())

# ARCH(1) - simpler, variance depends only on past errors
arch1 = arch_model(train_scaled, vol='ARCH', p=1)
arch1_result = arch1.fit()

# Forecast variance
forecasts = result.forecast(horizon=5)
variance_forecast = forecasts.variance[-1:]
```

**Gotcha**: Die Bibliothek `arch` warnt, wenn die Skalierung der Eingabe zu klein ist. Standardisieren Sie daher immer zuerst (Mittelwert abziehen, durch Standardabweichung teilen). Der Parameter `vol='ARCH'` muss explizit gesetzt werden, da der Standard GARCH ist.

### Prophet (Facebook/Meta) {#prophet-facebookmeta}

Zerlegbares Zeitreihenmodell: Trend + Saisonalität + Feiertage + Regressoren. Für Geschäftsprognosen entwickelt, mit automatischer Behandlung gängiger Muster.

```python
from prophet import Prophet

# Data must have columns: 'ds' (datetime) and 'y' (values)
df_prophet = df[['date', 'value']].rename(columns={'date': 'ds', 'value': 'y'})

# Basic model
m = Prophet()
m.fit(df_prophet)

# Create future dates and predict
future = m.make_future_dataframe(periods=365)  # daily
forecast = m.predict(future)

# Multiplicative seasonality (for series where amplitude grows with level)
m = Prophet(seasonality_mode='multiplicative')

# Monthly data - specify freq
future = m.make_future_dataframe(periods=12, freq='MS')

# Add country holidays
m = Prophet()
m.add_country_holidays(country_name='US')
m.fit(df_prophet)

# Add custom regressor (exogenous variable)
m = Prophet()
m.add_regressor('promo')
m.fit(df_train)
# future df must also contain 'promo' column
```

**Wichtige Parameter**: `growth='linear'|'logistic'`, `changepoint_prior_scale` (Flexibilität der Trendänderungen, Standard 0,05), `seasonality_prior_scale` (Stärke der Saisonalität), `n_changepoints` (Standard 25).

**Automatisches Verhalten**: Deaktiviert die tägliche Saisonalität bei Tagesdaten und die tägliche plus wöchentliche Saisonalität bei Monatsdaten. Prophet gibt während des Fits Meldungen über deaktivierte Komponenten aus.

### Random Walk {#random-walk}

Ein Random Walk ist: x_t = x_(t-1) + Rauschen. Jeder Wert ist der vorherige Wert plus ein zufälliger Schritt. Ein Spezialfall von ARIMA(0,1,0).

**Random-Walk-Hypothese**: Aktienkurse folgen einem Random Walk und sind daher grundsätzlich nicht vorhersagbar. Folgerungen:
- Die beste Prognose für den morgigen Kurs ist der heutige Kurs
- Renditen (Kursdifferenzen) sind nicht vorhersagbar, nicht die Kurse selbst
- Verwenden Sie **Renditen** (oder logarithmische Renditen) als Features für ML, nicht die Rohkurse

**Extrapolationsproblem**: Die meisten ML-Modelle (SVM, Random Forest, neuronale Netze) können nicht über den Wertebereich der Trainingsdaten hinaus extrapolieren. Liegen die Trainingskurse bei 100 bis 200, kann das Modell 250 nicht vorhersagen. Deshalb funktionieren Renditen (stationär, begrenzter Wertebereich) für ML besser als Rohkurse.

### Auto ARIMA {#auto-arima}

Automatisierte Ordnungsauswahl durch eine Rastersuche über Kombinationen von (p,d,q). Macht die manuelle Interpretation von ACF/PACF überflüssig, indem Kandidatenmodelle getestet und das beste nach AIC/BIC ausgewählt wird.

```python
from pmdarima import auto_arima

# Basic usage
model = auto_arima(y_train, seasonal=True, m=12,
                   stepwise=True, suppress_warnings=True,
                   trace=True)  # trace=True shows all models tested
print(model.summary())
forecast = model.predict(n_periods=12)
```

**Log-Transformations-Trick**: Hat die Reihe eine wachsende Varianz (die Amplitude wächst mit dem Niveau), wenden Sie vor dem Fitten eine Log-Transformation an. Das verbessert oft die Genauigkeit bei gleicher ARIMA-Ordnung:

```python
import numpy as np

df['log_values'] = np.log(df['values'])
model_log = auto_arima(df['log_values'][:train_end],
                       seasonal=True, m=12, trace=True,
                       suppress_warnings=True)
forecast_log = model_log.predict(n_periods=n_test)
forecast_original = np.exp(forecast_log)  # reverse the transform
```

**Wichtige Argumente**:

- `trace=True`: gibt alle Kandidatenmodelle und ihre AIC-Werte aus, nützlich zum Verständnis der Suche
- `suppress_warnings=True`: unterdrückt Konvergenzwarnungen schwacher Kandidaten
- `m`: saisonale Periode (12 für monatlich, 7 für täglich mit Wochenmuster, 52 für wöchentlich mit Jahresmuster)
- `stepwise=True`: schnellere heuristische Suche (Standard). Setzen Sie `False` für eine erschöpfende Rastersuche (langsamer, gelegentlich besser)
- `seasonal=True/False`: ob die saisonale ARIMA-Komponente (P,D,Q) einbezogen wird

**pmdarima muss separat installiert werden**. Es ist nicht in gängigen Python-Distributionen oder den meisten Cloud-Notebook-Umgebungen enthalten. Installation über `pip install pmdarima`.

## Feature Engineering für Zeitreihen {#feature-engineering-for-time-series}

Für ML-Ansätze (baumbasiert, neuronale Netze):

```python
# Lag features
for lag in [1, 7, 14, 30]:
    df[f'lag_{lag}'] = df['value'].shift(lag)

# Rolling statistics
df['rolling_mean_7'] = df['value'].rolling(7).mean()
df['rolling_std_7'] = df['value'].rolling(7).std()

# Calendar features
df['day_of_week'] = df['date'].dt.dayofweek
df['month'] = df['date'].dt.month
df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
```

## Validierung für Zeitreihen {#validation-for-time-series}

**Verwenden Sie niemals einen zufälligen Train/Test-Split**, da die zeitliche Reihenfolge wichtig ist. Verwenden Sie einen zeitbasierten Split.

```python
from sklearn.model_selection import TimeSeriesSplit

tscv = TimeSeriesSplit(n_splits=5)
for train_idx, test_idx in tscv.split(X):
    # train on past, test on future
    X_train, X_test = X[train_idx], X[test_idx]
```

### Walk-Forward-Validierung {#walk-forward-validation}

Die gründlichste Validierungsmethode für Zeitreihen. Trainieren Sie auf einem wachsenden Fenster, prognostizieren Sie die nächsten h Schritte, verschieben Sie das Fenster und wiederholen Sie den Vorgang. Dies simuliert den realen Einsatz, bei dem das Modell periodisch neu trainiert wird.

```python
from itertools import product

h = 12           # forecast horizon
n_steps = 10     # number of walk-forward steps

results = []
for i in range(n_steps):
    train_end = len(series) - h - n_steps + i + 1
    train = series[:train_end]
    test = series[train_end:train_end + h]

    model = ExponentialSmoothing(train, trend='add',
                                seasonal='mul', seasonal_periods=12,
                                use_boxcox=True).fit()
    pred = model.forecast(h)
    error = np.mean(np.abs(test - pred))
    results.append(error)

avg_mae = np.mean(results)
```

Kombinieren Sie dies mit einer Rastersuche über Modellparameter (Trendtyp, Saisonalitätstyp, Box-Cox) mithilfe von `itertools.product`, um die beste Konfiguration über alle Walk-Forward-Fenster hinweg zu finden.

**Gotcha**: Der Parameter `use_boxcox` in statsmodels akzeptiert `True`, `False` oder einen Float (Lambda-Wert). Die Zeichenkette `'log'` taucht in einigen Dokumentationen auf, führt aber zu einem Fehler. Verwenden Sie stattdessen `0` (Lambda=0 entspricht der Log-Transformation).

## Gotchas {#gotchas}
- Zufälliger Train/Test-Split = Datenleck (zukünftige Informationen im Training)
- Für ARIMA ist Stationarität erforderlich. Immer zuerst testen
- Die saisonale Periode muss bekannt sein (Domänenwissen oder ACF-Plot)
- Die Prognoseunsicherheit wächst mit dem Horizont. Geben Sie immer Konfidenzintervalle an
- Bei sehr langen Reihen können LSTMs/Transformer ARIMA übertreffen, benötigen aber deutlich mehr Daten
- **Die Schätzung von VARMA ist langsam und instabil**. Verwenden Sie für die meisten multivariaten Fälle VAR (ohne MA-Anteil) oder gehen Sie direkt zu ML-/DL-Ansätzen über
- **GARCH benötigt skalierte Eingaben**. Werte zwischen 1 und 1000, immer zuerst standardisieren
- **Prophet deaktiviert automatisch Saisonalität unterhalb der Datenfrequenz**. Monatsdaten können keine täglichen/wöchentlichen Muster erfassen. Das ist erwartetes Verhalten
- **Ökonometrische vs. ML-Validierung**: Die traditionelle Ökonometrie verzichtet oft auf Train/Test-Splits und prognostiziert über die verfügbaren Daten hinaus. Verwenden Sie immer eine saubere Out-of-Sample-Evaluierung
- **Prophet auf Aktienkursen** ist ein häufiger Fehler. Prophet ist für Geschäftskennzahlen mit ausgeprägter Saisonalität (Umsätze, Traffic) konzipiert, nicht für Finanzinstrumente, die einem Random Walk folgen. Aktienkursen fehlen die stabilen saisonalen Muster, auf die sich Prophet stützt, was zu stark fehlerhaften Prognosen führt
- **Auto ARIMA auf Aktien** liefert ebenso schlechte Ergebnisse. Die Random-Walk-Hypothese bedeutet, dass die beste Prognose „morgiger Kurs = heutiger Kurs" ist. Jedes Modell, das diese Prognose auf Out-of-Sample-Daten konsistent schlägt, sollte auf Datenleck hin überprüft werden
- **ACF/PACF für multivariate Reihen**: Die ACF/PACF pro Reihe ignoriert Kreuzkorrelationen. Verwenden Sie sie nur als grobe Orientierung und führen Sie anschließend eine Rastersuche über (p,q) durch
- **statsmodels `use_boxcox='log'` ist fehlerhaft**. Verwenden Sie `0` (Lambda=0 entspricht der Log-Transformation)

## Siehe auch {#see-also}
- [[rnn-sequences]] - Deep Learning für Sequenzen
- [[cnn-computer-vision]] - auf Zeitreihenklassifikation angewandte CNNs
- [[hypothesis-testing]] - Prüfung der Signifikanz eines Trends
- [[pandas-eda]] - Zeitreihenverarbeitung in pandas
- [[feature-engineering]] - Erstellung zeitbasierter Features
- [[model-evaluation]] - Details zur Walk-Forward-Validierung
- [[neural-networks]] - ANNs für Zeitreihenprognosen
