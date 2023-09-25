import mesa

from .model import MediaMultitasking

COLORS = {"Music": "#00AA00", "Homework": "#880000", "TV": "#000000", "Nothing": "#0088AA"}


def media_multitasking_portrayal(media):
    if media is None:
        return
    portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0}
    (x, y) = media.pos
    portrayal["x"] = x
    portrayal["y"] = y
    portrayal["Color"] = COLORS[media.condition]
    return portrayal


canvas_element = mesa.visualization.CanvasGrid(
    media_multitasking_portrayal, 30, 30, 300, 300
)
tree_chart = mesa.visualization.ChartModule(
    [{"Label": label, "Color": color} for (label, color) in COLORS.items()]
)
pie_chart = mesa.visualization.PieChartModule(
    [{"Label": label, "Color": color} for (label, color) in COLORS.items()]
)

model_params = {
    "height": 30,
    "width": 30,
    "density": mesa.visualization.Slider("People density", 0.10, 0.01, 1.0, 0.01),
}
server = mesa.visualization.ModularServer(
    MediaMultitasking, [canvas_element, tree_chart, pie_chart], "Media Multitasking", model_params
)
