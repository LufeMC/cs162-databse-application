from fakeData.createBuyers import createBuyers
from fakeData.createOffices import createOffices
from fakeData.createAgents import createAgents
from fakeData.createListings import createListings
from fakeData.createOrders import createOrders
from fakeData.createRates import createRates


def createFakeData(numBuyers, numOffices, numAgents, numListings, numOrders):
    createRates()
    createBuyers(numBuyers)
    createOffices(numOffices)
    createAgents(numAgents, numOffices)
    createListings(numListings)
    createOrders(numOrders, numListings, numAgents, numBuyers)
