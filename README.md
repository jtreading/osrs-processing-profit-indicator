# OSRS Profit Indicator

This is a python-based command-line tool for tracking real-time profit estimates based on item prices from the OSRS Wiki API. This allows users to monitor the profitability of item recipes by calculating profits based on the market values of input and output items. While this was primarily created to track profit for processing items, it may also be used to monitor profit for item flipping.

## Disclaimer

This tool is **not** a money-making guide, it is an efficiency aide. Several factors influence the profitability of processing recipes or flips: primarily volume and price volatility for both input and output items. It is **highly** recommended to be familiar with the mechanisms of the Grand Exchange and the general market conditions for the processing recipes or flips that you intend to use this tool to monitor.

Profit estimates do not take into account volume, price volatility, or time taken for orders to fill.

This tool provides information in the form of *estimates*, use at your own risk.

## Usage

#### Requirements

```
python >= 3.10.6
```

#### Setup

1. Clone this repository to your machine with git.
2. Create and activate a python virtual environment.
3. Install requirements from `requirements.txt` with pip.

#### Adding Recipes

(note: Currently, profit estimation for processing methods only supports one input item and one output item. This may be expanded in a future update.)

Processing:

Create a json file under the recipes folder with the following properties defined based on your method:

* input-item-name, type: str
* input-item-id, type: int
* output-item-name, type: str
* output-item-id, type: int
* output-per-input, type: int
* processed-per-hour, type: int

Item IDs may be found on the OSRS [Wiki Prices page](https://prices.runescape.wiki) (end of URL).

Flipping:

* Follow the same instructions as for processing, setting input and output item names and IDs to equivalent values and setting `output-per-input` to `1`. Set `processed-per-hour` to `1`. Understand that this will now track profit per item flipped instead of profit per hour of processing.

#### Running

`python app.py --recipe bracelet-to-ether --interval 30`

Output Sample:

````
----------
Buying Bracelet of ethereum (uncharged) at 42920 gp.
Selling Revenant ether at 180 gp.
Estimated profit for bracelet-to-ether: 3403120 gp/h.
----------
Buying Bracelet of ethereum (uncharged) at 43395 gp.
Selling Revenant ether at 180 gp.
Estimated profit for bracelet-to-ether: 2033220 gp/h.

````

# Planned Improvements:

- finish readme
- make recipe selectable from a list
- get polling interval from user input
