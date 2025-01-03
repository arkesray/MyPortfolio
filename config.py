import sys

config_dict = {
    "generate_history_symbol" : ["none", "required", "all"][0],
    "rpt_prefix" : ["","Personal/"][1]
}

try:
    config_dict["generate_history_symbol"] = ["none", "required", "all"][int(sys.argv[1])]
except:
    pass

save_path = './StockHistory/'
