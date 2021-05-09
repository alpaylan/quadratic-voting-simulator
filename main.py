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
            if delegate['bills'][bill['name']]['direction'] == 'left':
                if 50 <= delegate['bills'][bill['name']]['position']:
                    bill['vote'] += vote
                else:
                    bill['vote'] -= vote
            if delegate['bills'][bill['name']]['direction'] == 'right':
                if 50 > delegate['bills'][bill['name']]['position']:
                    bill['vote'] += vote
                else:
                    bill['vote'] -= vote


        print(f"Bill {bill['name']} is voted {bill['vote']}")


def simulation_individual_proportional_normal():
    global store
    for bill in store['bills']:
        for delegate in store['delegates']:
            current_difference = abs(delegate['bills'][bill['name']]['position'] - 50)
            total_difference = 0
            for b in store['bills']:
                total_difference += abs(delegate['bills'][b['name']]['position'] - 50)
            vote = get_closest_quad_value(store['vote_credits']*current_difference/total_difference)
            delegate['bills'][bill['name']]['vote'] = vote
            if delegate['bills'][bill['name']]['direction'] == 'left':
                if 50 <= delegate['bills'][bill['name']]['position']:
                    bill['vote'] += vote
                else:
                    bill['vote'] -= vote
            if delegate['bills'][bill['name']]['direction'] == 'right':
                if 50 > delegate['bills'][bill['name']]['position']:
                    bill['vote'] += vote
                else:
                    bill['vote'] -= vote


        print(f"Bill {bill['name']} is voted {bill['vote']}")


def position_print(bill, param):
    global store
    pos_str = "\n"
    for k, v in store[param]['bills'][bill['name']].items():
        pos_str += f"{k.capitalize()}: {v}\n"
    return pos_str


def result_print(bill):
    global store
    print("\n___________________Bill Info___________________")
    print(f"Congress Voted on {bill['name']}")
    print(f"Minority position on {bill['name']}:{position_print(bill, 'minority_position')}", end="")
    print(f"Majority position on {bill['name']}:{position_print(bill, 'majority_position')}", end="")
    print(f"{bill['name']} Bill was voted {bill['vote']}")


def simulation_individual_maximize_normal():
    global store
    for bill in store['bills']:
        for delegate in store['delegates']:
            max_bill = bill
            max_diff = 0
            for b in store['bills']:
                cur_diff = abs(delegate['bills'][b['name']]['position'] - 50)
                if cur_diff > max_diff:
                    max_diff = cur_diff
                    max_bill = b
            if bill == max_bill:
                vote = get_closest_quad_value(store['vote_credits'])
            else:
                vote = 0
            delegate['bills'][bill['name']]['vote'] = vote
            if delegate['bills'][bill['name']]['direction'] == 'left':
                if 50 <= delegate['bills'][bill['name']]['position']:
                    bill['vote'] += vote
                else:
                    bill['vote'] -= vote
            if delegate['bills'][bill['name']]['direction'] == 'right':
                if 50 > delegate['bills'][bill['name']]['position']:
                    bill['vote'] += vote
                else:
                    bill['vote'] -= vote

        result_print(bill)


def generate_delegates():
    import math
    import random

    if store['majority_position']['type'] == "constant":
        pass
    elif store['majority_position']['type'] == "normal":
        for d in range(store['majority']):
            delegate = {'party': 'majority', 'bills': {}}

            for name, params in store['majority_position']['bills'].items():
                mean = params['mean']
                std = math.sqrt(params['variance'])
                normal_dist = random.gauss(mean, std)

                delegate['bills'][name] = {
                    'position': normal_dist,
                    'direction': params['direction']
                }

            store['delegates'].append(delegate)

    elif store['majority_position']['type'] == "uniform":
        for d in range(store['majority']):
            delegate = {'party': 'majority', 'bills': {}}

            for name, params in store['majority_position']['bills'].items():
                a = params['a']
                b = params['b']
                uniform_dist = random.uniform(a, b)

                delegate['bills'][name] = {
                    'position': uniform_dist,
                    'direction': params['direction']
                }

            store['delegates'].append(delegate)
            print(delegate)

    if store['minority_position']['type'] == "constant":
        pass
    elif store['minority_position']['type'] == "normal":
        for d in range(store['minority']):
            delegate = {'party': 'minority', 'bills': {}}

            for name, params in store['minority_position']['bills'].items():
                mean = params['mean']
                std = math.sqrt(params['variance'])
                normal_dist = random.gauss(mean, std)

                delegate['bills'][name] = {
                    'position': normal_dist,
                    'direction': params['direction']
                }

            store['delegates'].append(delegate)

    elif store['minority_position']['type'] == "uniform":
        for d in range(store['minority']):
            delegate = {'party': 'minority', 'bills': {}}

            for name, params in store['minority_position']['bills'].items():
                a = params['a']
                b = params['b']
                uniform_dist = random.uniform(a, b)

                delegate['bills'][name] = {
                    'position': uniform_dist,
                    'direction': params['direction']
                }

            store['delegates'].append(delegate)
            print(delegate)

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


def plot_min_maj(bill):
    import plotly.graph_objects as go
    import pandas as pd

    minority_delegates = []
    for delegate in store['delegates']:
        if delegate['party'] == 'minority':
            minority_delegates.append(delegate['bills'][bill]['position'])
    x0 = pd.DataFrame(minority_delegates, columns=['position'])

    majority_delegates = []
    for delegate in store['delegates']:
        if delegate['party'] == 'majority':
            majority_delegates.append(delegate['bills'][bill]['position'])
    x1 = pd.DataFrame(majority_delegates, columns=['position'])

    fig = go.Figure()
    fig.add_trace(go.Histogram(x=x0.transpose().to_numpy()[0]))
    fig.add_trace(go.Histogram(x=x1.transpose().to_numpy()[0]))

    fig.add_vline(
        x=50.0,
        line_width=4,
        line_dash="dash",
        line_color="green",
        annotation_text=f"{bill} Bill",
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
    # simulation_individual_simple_normal()
    # simulation_individual_proportional_normal()
    simulation_individual_maximize_normal()
    # print(json.dumps(store, sort_keys=False, indent=4))
    f = open('store.json', 'w')
    f.write(json.dumps(store, sort_keys=False, indent=4))

    # plot_majority()
    # plot_minority()
    for bill in store['bills']:
        plot_min_maj(bill['name'])
