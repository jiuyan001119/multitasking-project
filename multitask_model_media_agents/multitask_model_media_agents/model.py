import mesa

from .agent import MediaCell

import numpy as np


class MediaMultitasking(mesa.Model):
    """
    Represents the transformations when agents are dealing with multitask situations.
    """

    def __init__(self, width=30, height=30, density=0.85):
        """
        Create a new environment model.

        Args:
            width, height: The size of the grid to model
            density: What fraction of grid cells have a media in them.
        """
        # Set up model objects
        self.schedule = mesa.time.RandomActivation(self)
        self.grid = mesa.space.SingleGrid(width, height, torus=False)

        self.datacollector = mesa.DataCollector(
            {
                "Music": lambda m: self.count_type(m, "Music"),
                "Homework": lambda m: self.count_type(m, "Homework"),
                "TV": lambda m: self.count_type(m, "TV"),
                "Nothing": lambda m: self.count_type(m, "Nothing"),
            }
        )

        # Place a tree in each cell with Prob = density
        for contents, (x, y) in self.grid.coord_iter():
            if self.random.random() < density:
                # Create a tree
                new_media = MediaCell((x, y), self)
                # Set all trees in the first column on fire.
                xlabel = np.random.randint(1,100,size=10)
                ylabel = np.random.randint(1,100,size=10)

                if x in xlabel[0:3] and y in ylabel[0:3]:
                    new_media.condition = "Music"
                    # self.grid.place_agent(new_media, (x, y))
                    # self.schedule.add(new_media)
                elif x in xlabel[3:6] and y in ylabel[3:6]:
                    new_media.condition = "Homework"
                    # self.grid.place_agent(new_media, (x, y))
                    # self.schedule.add(new_media)
                elif x in xlabel[6:10] and y in ylabel[6:10]:
                    new_media.condition = "TV"
                    # self.grid.place_agent(new_media, (x, y))
                    # self.schedule.add(new_media)
                self.grid.place_agent(new_media, (x, y))
                self.schedule.add(new_media)
        self.difference = 10000
        self.stable_index = 0
        # self.next_score = next_score
        self.running = True
        self.datacollector.collect(self)

    def step(self):
        """
        Advance the model by one step.
        """
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)

        # Halt if no more fire
        self.difference = abs(self.count_type(self, "Music") - 750)
        if self.difference <= 10:
            self.stable_index += 1
        if self.stable_index >=5:
            self.running = False
        # self.next_score = self.count_type(self, "Music")

        # return self.next_score

    @staticmethod
    def count_type(model, media_condition):
        """
        Helper method to count trees in a given condition in a given model.
        """
        count = 0
        for media in model.schedule.agents:
            if media.condition == media_condition:
                count += 1
        return count
