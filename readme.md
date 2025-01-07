# doku: markdown
## tests werden nicht mehr gemacht genug für heute

Link zur Anleitung: https://docs.github.com/de/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax

Here is a simple flow chart:

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
    n9 --> B
    roundedId@{ shape: proc}
    n7@{ shape: rect}
    n8@{ shape: rect}
    n9@{ shape: rect}
    n5@{ shape: rect}
```

