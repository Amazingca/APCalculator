B_TAX = 0.0225
T_TAX = 0.0805

if __name__ == "__main__":
    print("Apartment Payments Calculator: v0.1")
    parties = input("Enter the people involved, seperated by comma:\n>>> ").replace(" ", "").lower().split(",")
    print(f"Total parties: {len(parties)}")
    continueAddingItems = True
    items = []
    while (continueAddingItems):
        itemPrice = input("Enter a price for an item, or nothing to stop:\n>>> $")
        if (itemPrice == ""):
            continueAddingItems = False
            continue
        else:
            itemPrice = float(itemPrice)
            quantity = int(input("Enter item quantity:\n>>> "))
            taxType = input("Enter a tax type (B|T):\n>>> ").lower()
            while (taxType != "b" and taxType != "t"):
                taxType = input("This is not a valid tax type! Please try again...\n>>> ").lower()
            # extraDiscounts = input("Add extra discounts by percent:\n>>> ")
            involvedParties = input("Enter involved parties, seperated by comma:\n>>> ").replace(" ", "").lower().split(",")
            print(f"Here's the details about the item:\nPrice: ${itemPrice} (x{quantity})\nParties: {involvedParties}")
            items.append({
                "price": itemPrice,
                "quantity": quantity,
                "tax": taxType,
                "parties": involvedParties
            })
    discounts = input("Enter the percentage discounts applied to the order, sequentially, seperated by comma:\n>>> ").replace(" ", "").split(",")
    totals = {}
    for party in parties:
        totals[party] = []
    for item in items:
        item["price"] *= item["quantity"]
        if len(discounts) != 1 and discounts[1] != "":
            for discount in discounts:
                item["price"] *= 1 - (float(discount) / 100)
        item["price"] *= 1 + (B_TAX if item["tax"] == "b" else T_TAX)
        item["price"] /= len(item["parties"])
        for party in item["parties"]:
            totals[party].append(item["price"])
    grandTotal = 0.0
    for party in totals:
        print("=" * 24)
        print(f"{party:^24}")
        total = 0.0
        for price in totals[party]:
            total += price
            print(f"${price}")
        print(f"\n{f'Total: ${total:.2f}':>24}")
        grandTotal += total
    print(f"\n{f'Grand total: ${grandTotal:.2f}':>24}\n")
