// ===== CART FUNCTIONALITY =====
var cartItems = [];

function addToCart(dish, price) {
    var item = cartItems.find(i => i.name === dish);
    if (item) {
        item.qty++;
    } else {
        cartItems.push({ name: dish, price: price, qty: 1 });
    }
    updateCart();
}

function updateCart() {
    var tbody = document.querySelector("#cartTable tbody");
    if (tbody) {
        tbody.innerHTML = "";
        var grandTotal = 0;
        cartItems.forEach(function(item, index) {
            var total = item.price * item.qty;
            grandTotal += total;
            var row = `
                <tr>
                    <td>${item.name}</td>
                    <td>Rs. ${item.price}</td>
                    <td>${item.qty}</td>
                    <td>Rs. ${total}</td>
                    <td><button class="btn btn-xs btn-danger" onclick="removeItem(${index})">X</button></td>
                </tr>
            `;
            tbody.innerHTML += row;
        });
        document.getElementById("grandTotal").innerText = grandTotal;
    }
}

function removeItem(index) {
    cartItems.splice(index, 1);
    updateCart();
}

function openCart() {
    updateCart();
    document.querySelector('.overlay').style.display = 'block';
    document.getElementById('cartModal').style.display = 'block';
}

function closeCart() {
    document.querySelector('.overlay').style.display = 'none';
    document.getElementById('cartModal').style.display = 'none';
}

// ===== ORDER PAGE FUNCTIONALITY =====
const productdetails = {
    "Chicken Biryani": { price: 560, quantity: "1/2 KG"},
    "Beef Biryani": { price: 460, quantity: "1/2 KG"},
    "Mutton Biryani": { price: 950, quantity: "1/2 KG"},
    "Pulao": { price: 550, quantity: "1/2 KG"},
    "Nihari": { price: 600, quantity: "1/2 KG"},
    "Haleem": { price: 700, quantity: "1/2 KG"},
    "Chapli Kebab": { price: 950, quantity: "4 PCS"},
    "Seekh Kebab": { price: 820, quantity: "4 PCS"},
    "Karahi Chicken": { price: 850, quantity: "1/2 KG"},
    "Karahi Mutton": { price: 1200, quantity: "1/2 KG"},
    "Dum Pukht": { price: 13560, quantity: "Full"},
    "BBQ Tikka": { price: 600, quantity: "1/2 KG"},
    "Malai Boti": { price: 620, quantity: "1/2 KG"},
    "Beef Roll": { price: 470, quantity: "1 PCS"},
    "Chicken Roll": { price: 180, quantity: "1 PCS"},
    "Tandoori Chicken": { price: 1150, quantity: "1/2 KG"},
    "Paneer Tikka": { price: 1050, quantity: "1/2 KG"},
    "Chana Chaat": { price: 230, quantity: "1 Plate"},
    "Samosa": { price: 840, quantity: "12 PCS"},
    "Pakora": { price: 520, quantity: "1/2 KG"},
    "Paya": { price: 550, quantity: "1 Plate"},
    "Fish Fry": { price: 700, quantity: "1/2 KG"},
    "Prawn Masala": { price: 950, quantity: "1/2 KG"},
    "Shami Kebab": { price: 200, quantity: "4 PCS"},
    "Katakat": { price: 870, quantity: "1/2 KG"},
    "Mutton Ribs": { price: 900, quantity: "1/2 KG"},
    "Aloo Gosht": { price: 600, quantity: "1/2 KG"},
    "Chicken Handi": { price: 850, quantity: "1/2 KG"},
    "Butter Chicken": { price: 700, quantity: "1/2 KG"},
    "Chicken Jalfrezi": { price: 650, quantity: "1/2 KG"},
    "Beef Kofta": { price: 1900, quantity: "1/2 KG"},
    "Mutton Qorma": { price: 1100, quantity: "1/2 KG"},
    "Tawa Chicken": { price: 600, quantity: "1/2 KG"},
    "Makhni Handi": { price: 950, quantity: "1/2 KG"},
    "Kunna": { price: 1000, quantity: "1/2 KG"},
    "Sindhi Biryani": { price: 700, quantity: "1/2 KG"},
    "BBQ Platter": { price: 1800, quantity: "1/2 KG"},
    "Mix Grill": { price: 1500, quantity: "1/2 KG"},
    "Hyderabadi Biryani": { price: 750, quantity: "1/2 KG"},
    "Chicken Qeema": { price: 550, quantity: "1/2 KG"},
    "Bhuna Gosht": { price: 850, quantity: "1/2 KG"},
    "Anda Curry": { price: 400, quantity: "1/2 KG"},
    "Dal Makhni": { price: 450, quantity: "1/2 KG"},
    "Dal Tadka": { price: 350, quantity: "1/2 KG"},
    "Baingan Bharta": { price: 300, quantity: "1/2 KG"},
    "Gobi Aloo": { price: 280, quantity: "1/2 KG"},
    "Vegetable Biryani": { price: 400, quantity: "1/2 KG"},
    "Matar Paneer": { price: 450, quantity: "1/2 KG"},
    "Zarda": { price: 300, quantity: "1/2 KG"},
    "Sheer Khurma": { price: 350, quantity: "1 Plate"},
    "Kheer": { price: 280, quantity: "1 Plate"},
    "Shahi Tukray": { price: 320, quantity: "1 Plate"},
    "Ras Malai": { price: 500, quantity: "6 PCS"},
    "Gajar Ka Halwa": { price: 350, quantity: "1/2 KG"},
    "Fruit Trifle": { price: 400, quantity: "1/2 KG"}
};

function setPrice() {
    const product = document.getElementById("productname");
    const priceInput = document.getElementById("price");
    const quantity = document.getElementById("quantity");

    if (product && product.value in productdetails) {
        priceInput.value = productdetails[product.value].price;
        quantity.value = productdetails[product.value].quantity;
    } else if (priceInput && quantity) {
        priceInput.value = "";
        quantity.value = "";
    }
}

function updateTotalPrice() {
    const product = document.getElementById("productname");
    const quantity = document.getElementById("quantity");
    const priceInput = document.getElementById("price");

    if (product && product.value in productdetails && quantity && priceInput) {
        const unitPrice = productdetails[product.value].price;
        const selectedQty = parseInt(quantity.value) || 1;
        priceInput.value = unitPrice * selectedQty;
    }
}

function increaseQuantity() {
    const quantityInput = document.getElementById("quantity");
    if (quantityInput) {
        let currentQty = parseInt(quantityInput.value) || 1;
        currentQty++;
        quantityInput.value = currentQty;
        updateTotalPrice();
    }
}

function decreaseQuantity() {
    const quantityInput = document.getElementById("quantity");
    if (quantityInput) {
        let currentQty = parseInt(quantityInput.value) || 1;
        if (currentQty > 1) {
            currentQty--;
            quantityInput.value = currentQty;
            updateTotalPrice();
        }
    }
}

function toggleTransactionID() {
    const paymentMethod = document.getElementById("payment_mtd");
    const transactionField = document.getElementById("transaction_id_field");

    if (paymentMethod && transactionField) {
        if (paymentMethod.value === "Credit Card" || paymentMethod.value === "Debit Card" || 
            paymentMethod.value === "Bank Transfer" || paymentMethod.value === "Jazz Cash" || 
            paymentMethod.value === "EasyPaisa") {
            transactionField.classList.remove("hidden");
        } else {
            transactionField.classList.add("hidden");
        }
    }
}

// ===== RESERVATION PAGE FUNCTIONALITY =====
function toggleReservationTransactionID() {
    const paymentMethod = document.getElementById("payment");
    const transactionIDField = document.getElementById("transaction_id_field");

    if (paymentMethod && transactionIDField) {
        if (paymentMethod.value === "credit_card" || paymentMethod.value === "debit_card") {
            transactionIDField.classList.remove("hidden");
        } else {
            transactionIDField.classList.add("hidden");
        }
    }
}

function updateReservationAmount() {
    const guests = document.getElementById("guests");
    const amountField = document.getElementById("amount");
    const amountPerGuest = 3200;

    if (guests && amountField) {
        if (guests.value) {
            amountField.value = guests.value * amountPerGuest;
        } else {
            amountField.value = '';
        }
    }
}

// ===== INITIALIZATION =====
document.addEventListener('DOMContentLoaded', function() {
    // Initialize cart if needed
    updateCart();
    
    // Set up event listeners for order page
    const productSelect = document.getElementById("productname");
    if (productSelect) {
        productSelect.addEventListener('change', setPrice);
    }
    
    const quantityInput = document.getElementById("quantity");
    if (quantityInput) {
        quantityInput.addEventListener('change', updateTotalPrice);
        quantityInput.addEventListener('input', updateTotalPrice);
    }
    
    const paymentMethod = document.getElementById("payment_mtd");
    if (paymentMethod) {
        paymentMethod.addEventListener('change', toggleTransactionID);
    }
    
    // Set up event listeners for reservation page
    const reservationPaymentMethod = document.getElementById("payment");
    if (reservationPaymentMethod) {
        reservationPaymentMethod.addEventListener('change', toggleReservationTransactionID);
    }
    
    const guestsInput = document.getElementById("guests");
    if (guestsInput) {
        guestsInput.addEventListener('input', updateReservationAmount);
    }
});