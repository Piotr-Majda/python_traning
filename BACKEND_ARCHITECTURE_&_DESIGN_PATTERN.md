# Backend Architecture & Design Patterns

## Overview

Najczęstsze architektury backendowe - co to, kiedy używać, plusy i minusy.

---

## 1. Layered / N-tier (Architektura Warstwowa)

### Idea

Warstwy: **prezentacja → aplikacja/serwisy → domena → persystencja**

### Kiedy używać

- Proste do średnio złożonych systemów
- Pierwsze kroki w architekturze
- Zespoły uczące się dobrych praktyk

### ✅ Plusy

- Łatwo zacząć
- Czytelny podział odpowiedzialności
- Intuicyjne dla początkujących

### ❌ Minusy

- Z czasem "przecieki" zależności między warstwami
- Trudniej testować domenę w izolacji
- Może prowadzić do "anemic domain model"

---

## 2. Modular Monolith (Modułowy Monolit)

### Idea

Jeden deployment, ale kod podzielony na moduły domenowe (np. `accounts`, `instruments`, `transactions`)

### Kiedy używać

- 80% projektów na start
- Chcesz porządek bez kosztu mikroserwisów
- Zespoły 5-15 osób

### ✅ Plusy

- Proste wdrożenia
- Szybka zmiana
- Granice gotowe na przyszły podział na mikroserwisy

### ❌ Minusy

- Wymaga dyscypliny granic
- Ryzyko "big ball of mud"
- Trudne egzekwowanie izolacji modułów

---

## 3. Hexagonal / Ports & Adapters (Clean/Onion Architecture)

### Idea

Domena w centrum, wokół "porty" (interfejsy), a na brzegu "adaptery" (np. HTTP, DB, Kafka)

### Kiedy używać

- Chcesz testowalną domenę
- Łatwa wymiana technologii (DB/API)
- Złożona logika biznesowa

### ✅ Plusy

- Bardzo testowalne
- Elastyczne
- Izolacja logiki biznesowej

### ❌ Minusy

- Więcej "ceremonii" na start
- Krzywa uczenia się
- Może być over-engineering dla prostych projektów

---

## 4. DDD (Domain-Driven Design)

### Idea

Model domeny, bounded contexts, ubiquitous language

### Kiedy używać

- Złożona domena (finanse, zdrowie, logistyka)
- Duże zespoły z ekspertami domenowymi
- Długoterminowe projekty

### ✅ Plusy

- Klarowność pojęć i granic
- Lepsze zrozumienie biznesu
- Struktura dla złożonych systemów

### ❌ Minusy

- Nauka + dyscyplina
- Łatwo "przeteoretyzować"
- Wymaga ekspertów domenowych

---

## 5. Microservices

### Idea

Wiele małych serwisów, każdy za swój fragment domeny, komunikacja synch/async

### Kiedy używać

- Duże zespoły (15+ osób)
- Wysoka skala
- Niezależne tempo rozwoju modułów

### ✅ Plusy

- Niezależny deploy
- Skalowanie częściowe
- Różne technologie per serwis

### ❌ Minusy

- Złożoność operacyjna (K8s, sieć, obserwowalność)
- Transakcje rozproszone (saga pattern)
- Debugowanie między serwisami

---

## 6. Event-Driven Architecture

### Idea

Komunikacja przez zdarzenia (Kafka, RabbitMQ), luźne powiązanie

### Kiedy używać

- Integracje między systemami
- Audyt i logowanie
- Pipelines danych
- Reaktywność systemu

### ✅ Plusy

- Skalowalność
- Odporność na awarie
- Luźne powiązanie

### ❌ Minusy

- Złożona debugowalność
- Spójność ostateczna (eventual consistency)
- Trudne testowanie

---

## 7. CQRS (+ Event Sourcing)

### Idea

Rozdziel **Command** (zapis) i **Query** (odczyt); z ES zapisujesz zdarzenia zamiast stanu

### Kiedy używać

- Różne wymagania dla odczytu/zapisu
- Raportowanie i analityka
- Audyt zmian
- Wysoka wydajność odczytu

### ✅ Plusy

- Wydajny odczyt
- Historia zmian
- Optymalizacja per use case

### ❌ Minusy

- Większa złożoność
- Trzeba pamiętać o spójności
- Krzywa uczenia się

---

## 8. Serverless (FaaS)

### Idea

Funkcje w chmurze (AWS Lambda), płacisz za wykonanie

### Kiedy używać

- Zdarzenia i webhooks
- Batch/cron jobs
- Niska stała przepustowość
- Prototypowanie

### ✅ Plusy

- Brak serwerów do zarządzania
- Auto-skalowanie
- Płatność za użycie

### ❌ Minusy

- Cold starts
- Limity czasu/pamięci
- Lokalny dev bywa trudny
- Vendor lock-in

---

## 🎯 Wybór Architektury

### Dla początkujących

1. **Layered** → **Modular Monolith** → **Hexagonal**

### Dla zaawansowanych

1. **Hexagonal** → **DDD** → **Microservices** (jeśli potrzeba)

### Dla skalowania

1. **Event-Driven** + **CQRS** + **Microservices**

---

## 📚 Dodatkowe Zasoby

- [Clean Architecture - Robert Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Domain-Driven Design - Eric Evans](https://domainlanguage.com/ddd/)
- [Building Microservices - Sam Newman](https://samnewman.io/books/building_microservices/)
- [Patterns of Enterprise Application Architecture - Martin Fowler](https://martinfowler.com/books/eaa.html)
