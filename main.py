# Tax categories by item – To my knowledge, food items are taxed lower since they are considered essentials.
B_TAX = 0.0225
T_TAX = 0.0805

# All possibles responses that one can give to say "yes" to the receipt export prompt
TRUE_TYPES = ["true", "t", "yes", "y"]

if __name__ == "__main__":
    print("Apartment Payments Calculator: v1.0")
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
        totals[party] = [] # Initializes an empty array for each party that is involved in the "totals" dictionary
    for item in items:
        item["price"] *= item["quantity"] # Sets price to that of the original cost times quantity
        if len(discounts) != 1 and discounts[1] != "": # Assuming we have discounts to apply, we apply them in proceeding order to the item price
            for discount in discounts:
                item["price"] *= 1 - (float(discount) / 100) # Converts percentage discount to valid decimal and applies it to the item price
        item["price"] *= 1 + (B_TAX if item["tax"] == "b" else T_TAX) # Applied associated taxes based on the given tax type
        item["price"] /= len(item["parties"]) # Divides the cost amongst the associated parties
        for party in item["parties"]: # Applies the divides cost to each associated party's receipt
            totals[party].append(item["price"])
    grandTotal = 0.0
    for party in totals:
        print("=" * 24)
        print(f"{party:^24}") # Center-align party name in-between 24 chars
        total = 0.0
        for price in totals[party]:
            total += price
            print(f"${price}")
        print(f"\n{f'Total: ${total:.2f}':>24}") # Right-align party total to 24 chars
        grandTotal += total
    print(f"\n{f'Grand total: ${grandTotal:.2f}':>24}\n") # Right-align grand total to 24 chars
    export = input("Would you like to export this transaction to a file?\n>>> ").lower()
    if export in TRUE_TYPES:
        #location = input("Choose location...\n>>> ") (location + "ap_receipt.txt") if location[-1] == "/" else (location + "/ap_receipt.txt")
        # Essentially the same as above, though instead appends to a file instead of printing to console
        with open("ap_receipt.txt", "a") as f:
            for party in totals:
                print("=" * 24, file=f)
                print(f"{party:^24}", file=f)
                total = 0.0
                for price in totals[party]:
                    total += price
                    print(f"${price}", file=f)
                print(f"\n{f'Total: ${total:.2f}':>24}", file=f)
            print(f"\n{f'Grand total: ${grandTotal:.2f}':>24}\n", file=f)
