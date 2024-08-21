from datetime import date

# Tax categories by item – To my knowledge, food items are taxed lower since they are considered essentials.
B_TAX = 0.0225
T_TAX = 0.0805
D_TAX = 0.029

# All possibles responses that one can give to say "yes" to the receipt export prompt
TRUE_TYPES = ["true", "t", "yes", "y"]

# Prints the totals in receipt form to the console, and optionally to to specified file
def printTotals(totals, totalDiscount, f):
    grandTotal = 0.0
    for party in totals:
        print("=" * 26, file=f)
        print(f"{party[0].upper()+party[1:]:^26}", file=f) # Center-align party name in-between 24 chars
        total = 0.0
        for item in totals[party]:
            total += item["totalPrice"]
            preTotalText = f"""${item["price"]:.2f}{f" (x{item['quantity']})" if item["quantity"] > 1 else ""}""" # Line that contains basic information about the item - we need the length of it for proper right-side alignment which is why we are initializing it here
            print(f"""{preTotalText}{f"${item['totalPrice']:.2f}":>{24 - len(preTotalText)}}{f" {item['tax'].upper() if item['tax'] != '' else ''}"}""", file=f)
        print(f"\n{f'Total: ${total:.2f}':>24}", file=f) # Right-align party total to 24 chars
        grandTotal += total
    if totalDiscount != None:
        print(f"\n{f'Total discount: {(1 - totalDiscount) * 100:.2f}%':>24} -", file=f) # Right-align total discount to 24 chars
    print(f"\n{f'Grand total: ${grandTotal:.2f}':>24}\n", file=f) # Right-align grand total to 24 chars

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
            quantity = input("Enter item quantity:\n>>> ")
            quantity = int(quantity) if quantity != "" else 1
            taxType = input("Enter a tax type (B|T|D) or nothing for no tax:\n>>> ").lower()
            while (taxType != "b" and taxType != "t" and taxType != "d" and taxType != ""):
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
    totalDiscount = None
    if len(discounts) >= 1 and discounts[0] != "": # Assuming we have discounts to apply, we apply them in proceeding order to the item price
        totalDiscount = 1.0
        for discount in discounts:
            totalDiscount *= 1 - (float(discount) / 100) # Converts percentage discount to valid decimal and applies it to the total discount
    totals = {}
    for party in parties:
        totals[party] = [] # Initializes an empty array for each party that is involved in the "totals" dictionary
    for item in items:
        originalPrice = item["price"]
        item["price"] *= item["quantity"] # Sets price to that of the original cost times quantity
        if totalDiscount != None:
            item["price"] *= totalDiscount
        item["price"] *= 1 + (B_TAX if item["tax"] == "b" else T_TAX if item["tax"] == "t" else D_TAX if item["tax"] == "d" else 0) # Applies associated taxes based on the given tax type
        item["price"] /= len(item["parties"]) # Divides the cost amongst the associated parties
        for party in item["parties"]: # Applies the divides cost to each associated party's receipt
            totals[party].append({
                "price": originalPrice,
                "totalPrice": item["price"],
                "quantity": item["quantity"],
                "tax": item["tax"]
            })
    printTotals(totals, totalDiscount, None)
    export = input("Would you like to export this transaction to a file?\n>>> ").lower()
    if export in TRUE_TYPES:
        with open(f"ap_{date.today()}.txt", "a") as f:
            printTotals(totals, totalDiscount, f);
