## Apartment Payments Calculator (APCalculator)

This Python script is meant to ease the process of splitting payments for things with roommates. This is especially useful for large receipts and discounts applied to the entire purchase.

### Tax calculation

As shown in `main.py`, a CSV (`/taxes.csv`) is used to indicate the tax type and the percent of that tax (in decimal form.)

```csv
a,0.05
b,0.07
```

Use the characters "a" or "b" to reference the tax type for the item when you're adding it.

Conveniently, you can also export your transactions to a text file for easy sharing. You can find an example at `/example/ap_2024-12-18.txt` using the example taxes file above.