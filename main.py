store = dict()

def info_print():
    global store
    print("\n___________________Info___________________")
    print(f"You created a congress with size {store['size']}")
    print(f"You have {store['majority']} delegates from one party, and {store['minority']} delegates from the other")
    print(f"Majority to Minority ratio is {store['majority']/store['minority']:.2f}\n")


def get_closest_quad_value(val):
    import math
    sq_val = val**0.5
    return math.floor(sq_val)


def simulate_simple():
    global store
    vote = get_closest_quad_value(store['vote_credits'])
    for bill in store['bills']:
        if bill['position'] < store['majority_position']:
            bill['vote'] -= vote*store['majority']
        else:
            bill['vote'] += vote*store['majority']

        if bill['position'] > store['minority_position']:
            bill['vote'] -= vote*store['minority']
        else:
            bill['vote'] += vote*store['minority']

        print(f"Bill {bill['name']} is voted {bill['vote']}")


def simulation_distorted():
    import random
    global store
    vote = get_closest_quad_value(store['vote_credits'])
    for bill in store['bills']:
        if bill['position'] + random.randint(0, 12) < store['majority_position']:
            bill['vote'] -= vote*store['majority']
        else:
            bill['vote'] += vote*store['majority']

        if bill['position'] > store['minority_position']:
            bill['vote'] -= vote*store['minority']
        else:
            bill['vote'] += vote*store['minority']

        print(f"Bill {bill['name']} is voted {bill['vote']}")


def simulation_individual_simple_normal():
    global store
    vote = get_closest_quad_value(store['vote_credits'])
    for bill in store['bills']:
        for delegate in store['delegates']:
            if delegate['party'] == 'majority':
                if bill['position'] >= delegate['position']:
                    bill['vote'] += vote
                else:
                    bill['vote'] -= vote
            if delegate['party'] == 'minority':
                if bill['position'] <= delegate['position']:
                    bill['vote'] += vote
                else:
                    bill['vote'] -= vote

        print(f"Bill {bill['name']} is voted {bill['vote']}")


def generate_delegates():
    import math
    import random

    if store['majority_position']['type'] == "constant":
        pass
    elif store['majority_position']['type'] == "normal":
        mean = store['majority_position']['params']['mean']
        std = math.sqrt(store['majority_position']['params']['variance'])
        for delegate in range(store['majority']):
            normal_dist = random.gauss(mean, std)
            store['delegates'].append({'party': 'majority', 'position': normal_dist})
    elif store['majority_position']['type'] == "uniform":
        a = store['majority_position']['params']['a']
        b = math.sqrt(store['majority_position']['params']['b'])
        for delegate in range(store['majority']):
            uniform_dist = random.uniform(a, b)
            store['delegates'].append({'party': 'majority', 'position': uniform_dist})

    if store['minority_position']['type'] == "constant":
        pass
    elif store['minority_position']['type'] == "normal":
        mean = store['minority_position']['params']['mean']
        std = math.sqrt(store['minority_position']['params']['variance'])
        for delegate in range(store['minority']):
            normal_dist = random.gauss(mean, std)
            store['delegates'].append({'party': 'minority', 'position': normal_dist})
    elif store['minority_position']['type'] == "uniform":
        a = store['minority_position']['params']['a']
        b = math.sqrt(store['minority_position']['params']['b'])
        for delegate in range(store['minority']):
            uniform_dist = random.uniform(a, b)
            store['delegates'].append({'party': 'minority', 'position': uniform_dist})

    # print(store['delegates'])


def plot_majority():
    import plotly.graph_objects as go
    import pandas as pd
    import numpy as np

    majority_delegates = []
    for delegate in store['delegates']:
        if delegate['party'] == 'majority':
            majority_delegates.append(delegate['position'])
    x1 = pd.DataFrame(majority_delegates, columns=['position'])

    fig = go.Figure()
    fig.add_trace(go.Histogram(x=x1.transpose().to_numpy()[0]))

    # The two histograms are drawn on top of another
    # Overlay both histograms
    fig.update_layout(barmode='overlay')
    # Reduce opacity to see both histograms
    fig.update_traces(opacity=0.70)
    fig.show()

def plot_minority():
    import plotly.graph_objects as go
    import pandas as pd

    minority_delegates = []
    for delegate in store['delegates']:
        if delegate['party'] == 'minority':
            minority_delegates.append(delegate['position'])
    x0 = pd.DataFrame(minority_delegates, columns=['position'])
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=x0.transpose().to_numpy()[0]))

    # The two histograms are drawn on top of another
    # Overlay both histograms
    fig.update_layout(barmode='overlay')
    # Reduce opacity to see both histograms
    fig.update_traces(opacity=0.70)
    fig.show()


def plot_min_maj():
    import plotly.graph_objects as go
    import pandas as pd

    minority_delegates = []
    for delegate in store['delegates']:
        if delegate['party'] == 'minority':
            minority_delegates.append(delegate['position'])
    x0 = pd.DataFrame(minority_delegates, columns=['position'])

    majority_delegates = []
    for delegate in store['delegates']:
        if delegate['party'] == 'majority':
            majority_delegates.append(delegate['position'])
    x1 = pd.DataFrame(majority_delegates, columns=['position'])

    fig = go.Figure()
    fig.add_trace(go.Histogram(x=x0.transpose().to_numpy()[0]))
    fig.add_trace(go.Histogram(x=x1.transpose().to_numpy()[0]))

    for bill in store['bills']:
        fig.add_vline(
            x=bill['position'],
            line_width=4,
            line_dash="dash",
            line_color="green",
            annotation_text=f"{bill['name']} Bill",
            annotation_position="top left",
            annotation=dict(font_size=20, font_family="Times New Roman")
        )
    # The two histograms are drawn on top of another
    # Overlay both histograms
    fig.update_layout(barmode='overlay')
    # Reduce opacity to see both histograms
    fig.update_traces(opacity=0.70)

    fig.show()


def clear_past():
    store['delegates'].clear()
    for bill in store['bills']:
        bill['vote'] = 0


if __name__ == '__main__':
    import json
    f = open('store.json')
    fr = str(f.read())
    store = json.loads(fr)
    # print(store)
    if not store['active']:
        store['size'] = int(input("Number of Delegates: "))
        store['majority'] = int(input("Number of Delegates From The Majority Party: "))
        store['minority'] = store['size'] - store['majority']
        info_print()

        store['majority_position'] = int(input("From 0 to 100, define a position for the majority party in the political spectrum: "))
        store['minority_position'] = int(input("From 0 to 100, define a position for the minority party in the political spectrum: "))

        store['number_of_bills'] = int(input("Enter the number of bills to be discussed in congress: "))
        store['bills'] = []
        for i in range(store['number_of_bills']):
            bill_name = input("Enter the name of the bill: ")
            bill_position = int(input("From 0 to 100, define a position for the bill in the political spectrum: "))
            store['bills'].append({"name": bill_name, "position": bill_position, "vote": 0})

        store['vote_credits'] = int(input("Enter the amount of vote credits for each delegate: "))
    else:
        info_print()

    clear_past()
    generate_delegates()

    # simulate_simple()
    # simulation_distorted()
    simulation_individual_simple_normal()
    # print(json.dumps(store, sort_keys=False, indent=4))
    f = open('store.json', 'w')
    f.write(json.dumps(store, sort_keys=False, indent=4))

    # plot_majority()
    # plot_minority()
    plot_min_maj()
