import streamlit as st
import os

st.title("🧾 Singapore Cash Receipting App")

# Input fields
amount_payable = st.number_input("Enter Amount Payable (SGD)", min_value=0.00, format="%.2f")
amount_tendered = st.number_input("Enter Amount Tendered (SGD)", min_value=0.00, format="%.2f")

# Calculate change
change = round(amount_tendered - amount_payable, 2)
if change > 0:
    st.success(f"Change to be returned: ${change:.2f}")
elif change < 0:
    st.error(f"Insufficient amount tendered. You still owe: ${-change:.2f}")
else:
    st.info("Exact amount tendered. No change to be returned.")

#Store the receipt number
if "receipt_number" not in st.session_state:
    st.session_state.receipt_number = 10000 

#Create receipt record if change is to be returned
if change > 0:
    st.session_state.receipt_number += 1
    receipt = f"{st.session_state.receipt_number},{amount_payable:.2f},{amount_tendered:.2f},{change:.2f}\n"

# Add header/receipt record into file
    file_path = "collections.txt"
    file_is_empty = not os.path.exists(file_path) or os.path.getsize(file_path) == 0
    
    with open(file_path, "a") as file:
        if file_is_empty:
            file.write("Receipt No,Amount Payable,Amount Tendered,Change\n")
        file.write(receipt)

# list to store notes and coins dispensed
remaining = change
notes = [50,20,10,5,2]
note_dispensed = []
coins = [1,0.50,0.20,0.10,0.05]
coin_dispensed = []

# Notes dispensed
st.subheader("💵 Notes Dispensed")

if change > 0:
    for note in notes:
        count = int(remaining // note)
        remaining = round(remaining - count * note, 2)
        note_dispensed.append((count))
        st.write(f"{count} × ${note} note")

# Coins dispensed
st.subheader("🪙 Coins Dispensed")

if change > 0:
    for coin in coins:
        count = int(remaining // coin)
        remaining = round(remaining - count * coin, 2)
        coin_dispensed.append((count))
        st.write(f"{count} × ${coin:.2f} coin")
