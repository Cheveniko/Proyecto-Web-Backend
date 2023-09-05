import seatsio

client = seatsio.Client(seatsio.Region.SA(), secret_key='3675e545-9ec7-4a50-8b5f-9707cb85f058')
# chart = client.charts.create()
# event = client.events.create(chart.key)

def reservar(asientos):
    try:
        print(asientos)
        # client.events.book(event.key, ["A-1", "A-2"])
        client.events.book('Poliflight', ["A-1", "A-2"])
    except Exception as e:
        print(e)