# tkinter module to help in creating widgets for the store
import tkinter as tk
from tkinter.font import Font
from tkinter import *  
from tkinter import messagebox
from random import randint as rnd
import xml.etree.ElementTree as et

# class item
class Item:
    def __init__(self, name, price): 
        self.name = name
        self.price = price

# class shopping cart
class ShoppingCart:
    def __init__(self):
        """ initialize the shopping cart"""
        self.items = []

    # add items to the cart
    def addToCart(self, item): 
        self.items.append(item)

    # remove items from the cart
    def removeFromCart(self, itemIndex):
        self.items.pop(itemIndex)

    # total price for the items
    def getTotalPrice(self):
        totalPrice = 0
        for item in self.items:
            totalPrice += item.price
        return totalPrice

    # retrieve all items in the cart
    def getCartItems(self):
        return self.items

    #  clear the cart once the user has bought the items
    def emptyCart(self):
        self.items.clear()


# class store
class Store:
    def __init__(self):
        """ initialize the store items"""
        self.storeItems = []
        self.itemNames = ["HDMI Cable", "Keyboard", "Headphone", "RAM", "Mouse"]
        self.readStoreItems("products.xml")

    def readStoreItems(self, storeFileName):
        try:
            root =  et.parse(storeFileName).getroot()  
            for child in root.findall("product") : 
                self.storeItems.append(Item(  child.find("name").text, float( child.find("price").text) ) )

        except IOError:
            print("Store File Not Exists... Generating Random Store")
            self.generateRandomStoreItems(8)
    def getStoreItems(self):
        return self.storeItems

    def listStore(self):
        counter = 0
        print("Store Items : ") 
        for item in self.storeItems:
            print ("%s : %s  $%s" % (counter, item.name,item.price) )   
            counter += 1        
        print("")

    # generate random store items 
    def generateRandomStoreItems(self, amt):
        storedItemCounter = 0
        while (storedItemCounter < amt):
            itemName = self.itemNames[rnd(0, len(self.itemNames) - 1)]
            itemPrice = rnd(10, 100)
            newItem = Item( name=itemName, price=itemPrice)
            self.storeItems.append(newItem)
            storedItemCounter = storedItemCounter + 1


# viewstore function to display items in the store
def viewStore():
    global storeWindow 
    storeLabelFrame = LabelFrame(storeWindow, text="Store Items")
    storeLabelFrame.pack(fill="both", expand="yes", padx="20", pady="10")

    storeItemsFrame = Frame(storeLabelFrame)
    storeItemsFrame.pack(padx="10", pady="5")
    store = Store()
    storeItems = store.getStoreItems() 
    for item in storeItems:
        itemFrame = Frame(storeItemsFrame,  pady="5")
        itemFrame.pack(fill="both", expand="yes")

        nameLabel = Label(itemFrame, text=item.name,font=("Candara",15),fg="blue")
        priceLabel = Label(itemFrame, text="$ %s"%item.price , font=("Candara",13),fg="red")  
        addToCartBtn = Button(itemFrame, text="Add To Cart",cursor="hand2", command=lambda i=item: addItemToCart(i) ) 
        btnImage=PhotoImage(file="images/addToCart.png")       
        addToCartBtn.image= btnImage
        addToCartBtn.config(image=btnImage,width="40",height="40")

        nameLabel.pack(side="left")
        priceLabel.pack(side="left",fill="both", expand="yes" )
        addToCartBtn.pack(side="right" )

    btnGoCart = Button(storeWindow, text="Go To Cart", font=("Candara",15,"bold"),fg="red",bg="grey",cursor="hand2",relief=FLAT, command=viewCart )
    btnGoCart.pack(pady="6")

# viewcart function to display items that have been added to the cart
def viewCart():   
    cartWindow = Toplevel()
    cartWindow.title("The Cart")
    cartWindow.configure(bg="black")
    cartWindow.minsize(300,300)
    menu = Menu(cartWindow)
    cartWindow.config(menu=menu)
    subMenu = Menu(menu)
    menu.add_cascade(label = "File", menu= subMenu)
    subMenu.add_command(label = "New cart" )
    cartWindow.grab_set()
    global cart
    cartItems = cart.getCartItems()

    cartItemsLabelFrame = LabelFrame(cartWindow,text="Cart Items")
    cartItemsLabelFrame.pack(fill="both", expand="yes", padx="20", pady="10")

    cartItemsFrame = Frame(cartItemsLabelFrame, padx=3, pady=3)
    cartItemsFrame.pack()
    index = 0
    for item in cartItems:
        itemFrame = Frame(cartItemsFrame,  pady="5")
        itemFrame.pack(fill="both", expand="yes")

        nameLabel = Label(itemFrame, text=item.name,font=("Candara",15),fg="blue")
        priceLabel = Label(itemFrame, text="$ %s"%item.price,font=("Candara",13),fg="red")  
        addToCartBtn = Button(itemFrame, text="Remove From Cart", font=("Candara",11,"bold"),fg="red",bg="white",cursor="hand2", command=lambda i=index: removeFromCart(i,cartWindow) )

        nameLabel.pack(side="left")
        priceLabel.pack(side="left")
        addToCartBtn.pack(side="right" )
        index += 1

    checkOutFrame = Frame(cartWindow, pady="10")
    totalPriceLabel = Label(checkOutFrame, text="Total Price : $ %s" % cart.getTotalPrice(), font=("Candara",14,"bold"),fg="indigo")
    totalPriceLabel.pack(side="left")
    buyBtn = Button(checkOutFrame, text="Buy Now", font=("Candara",15,"bold"),fg="indigo",bg="white",cursor="hand2", command=lambda : buyCommand(cartWindow))
    buyBtn.pack(side="left",padx="10")
    checkOutFrame.pack()

    backToStoreBtn = Button(cartWindow, text="Back To Store", font=("Candara",15,"bold"),fg="red",bg="white",cursor="hand2",command=cartWindow.destroy)
    backToStoreBtn.pack(pady="6")
    backToStoreBtn = Button(cartWindow, text="receipt", font=("Candara",15,"bold"),fg="red",bg="white",cursor="hand2",command=receipt)
    backToStoreBtn.pack(pady="6")

    cartWindow.mainloop()

# receipt fucntion to generate the receipt 
def receipt():   
    receiptWindow = Toplevel()
    receiptWindow.title("receipt")
    receiptWindow.configure(bg="black")
    receiptWindow.minsize(300,300)
    menu = Menu(receiptWindow)
    receiptWindow.config(menu=menu)
    subMenu = Menu(menu)
    menu.add_cascade(label = "File", menu= subMenu)
    subMenu.add_command(label = "print" )
    receiptWindow.grab_set()
    global cart
    cartItems = cart.getCartItems()

    cartItemsLabelFrame = LabelFrame(receiptWindow,text="items bought")
    cartItemsLabelFrame.pack(fill="both", expand="yes", padx="20", pady="10")

    cartItemsFrame = Frame(cartItemsLabelFrame, padx=3, pady=3)
    cartItemsFrame.pack()
    index = 0
    for item in cartItems:
        itemFrame = Frame(cartItemsFrame,  pady="5")
        itemFrame.pack(fill="both", expand="yes")

        nameLabel = Label(itemFrame, text=item.name,font=("Candara",15),fg="blue")
        priceLabel = Label(itemFrame, text="$ %s"%item.price,font=("Candara",13),fg="red")  

        nameLabel.pack(side="left")
        priceLabel.pack(side="left")
        index += 1

    checkOutFrame = Frame(receiptWindow, pady="10")
    totalPriceLabel = Label(checkOutFrame, text="Total Price : $ %s" % cart.getTotalPrice(), font=("Candara",14,"bold"),fg="indigo")
    totalPriceLabel.pack(side="left")
    checkOutFrame.pack()

    receiptWindow.mainloop()


# additemtocart function to add items to the cart
def addItemToCart(item=None):
    global cart
    cart.addToCart(item)
    messagebox.showinfo(title="Success" , message="Item %s Added To The Cart !!"%item.name )

#  removefromcart function to remove items from the cart 
def removeFromCart(itemIndex=None,cartWindow=None):
    global cart
    cart.removeFromCart(itemIndex)
    messagebox.showinfo(title="success",message="Item Removed")
    cartWindow.destroy()
    viewCart()

#  buycommand function which will be passed in the buy now button as a command
def buyCommand(cartWindow):
    global cart
    cart.emptyCart()
    cartWindow.destroy()    
    messagebox.showinfo(title="success",message="Purchase Completed Successfully")

storeWindow = tk.Tk()
storeWindow.minsize(600,600)
storeWindow.title("online store")
storeWindow.iconbitmap('store.ICO')
storeWindow.configure(bg="black")
# menu bar section
# the top menu bar for the application
menu = Menu(storeWindow)
storeWindow.config(menu=menu)
subMenu = Menu(menu)
menu.add_cascade(label = "File", menu= subMenu)
subMenu.add_command(label = "quit", command=quit )


helpMenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpMenu)
helpMenu.add_command(label=" help" )

aboutusMenu = Menu(menu)
menu.add_cascade(label="About Us", menu=aboutusMenu)
aboutusMenu.add_command(label="about us")

viewMenu = Menu(menu)
menu.add_cascade(label="view", menu=viewMenu)
viewMenu.add_command(label="Items")
viewMenu.add_command(label="continue to cart")

itemsMenu = Menu(menu)
menu.add_cascade(label="Categories", menu=itemsMenu)
itemsMenu.add_command(label="Electronics")
itemsMenu.add_command(label="Fruits & vegetables", command=viewStore)
itemsMenu.add_command(label="Toys")
itemsMenu.add_command(label="Furniture")
itemsMenu.add_command(label="Fashion")



label = Label(storeWindow, text = "ONLINE STORE ")
label.pack()

# we call the view store function to display all the items available in the store
viewStore()

# an instance of the class Shoppingcart
cart = ShoppingCart() 

storeWindow.mainloop()
