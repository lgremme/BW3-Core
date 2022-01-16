# <center>Divera 24/7</center> 
---

## Beschreibung
Mit diesem Plugin ist es moeglich, Http-Anfragen für Alarmierungen an Divera 24/7 zu senden.
Wildcards in den Urls werden automatisch ersetzt.

## Unterstütze Alarmtypen
- Fms
- Pocsag
- Zvei
- Msg

## Resource
`divera`

## Konfiguration
|Feld|Beschreibung|Default|
|----|------------|-------|
|fms|Liste mit Urls für Fms-Alarmierung||
|pocsag|Liste mit Urls für Pocsag-Alarmierung||
|zvei|Liste mit Urls für Zvei-Alarmierung||
|msg|Liste mit Urls für Msg-Alarmierung||

**Beispiel:**
```yaml
  - type: plugin
    name: Divera Plugin
    res: divera
    config:
      accesskey: ajdlkfjsdklfjlksjflskdjf
      pocsag:
        priority: FALSE
        title_pocsag: {RIC}({SRIC})\n{MSG}
        message_pocsag: {MSG}
        # RIC ist in Divera definiert
        ric_pocsag: Probealarm
      fms:
        priority: FALSE
        title_fms: {FMS}
        message_fms: {FMS}
        vehicle: MTF
     zvei:
       ric_zvei: Probealarm
       title_zvei: {TONE}
       message_zvei: {TONE}
       priority: FALSE
     msg:
       priority: FALSE
        title_msg: {MSG}
        message_msg: {MSG}
        # RIC ist in Divera definiert
        ric_msg: Probealarm
      
```

---
## Modul Abhängigkeiten
- keine

---
## Externe Abhängigkeiten
- asyncio
- aiohttp
- urllib
