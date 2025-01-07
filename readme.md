# doku

```mermaid

---
config:
  theme: default
  look: handDrawn
---
flowchart TD
    roundedId["Backwheel"] --> B("basisklassen.py")
    n7["Frontwheel"] --> B
    n8["Infrared"] --> B
    rectId["Main"] --> n9["BaseCar"]
    n5["Ultrasonic"] --> B
    B <--> n9
    roundedId@{ shape: proc}
    n7@{ shape: rect}
    n8@{ shape: rect}
    n9@{ shape: rect}
    n5@{ shape: rect}
```

