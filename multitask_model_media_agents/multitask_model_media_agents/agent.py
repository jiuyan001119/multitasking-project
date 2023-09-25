import mesa
import numpy as np
# probability, step term, attention, enjoyment, audio, vision
# 0          , 1        , 2        , 3        , 4    , 5
all_multitask0 = {'music'   :[1, 0, 0, 1, 1, 0],
                  'TV'      :[1, 0, 0, 1, 1, 1],
                  'reading' :[1, 0, 0, 1, 0, 1],
                  'painting':[1, 0, 0, 1, 0, 1],
                  'computer':[1, 0, 0, 1, 1, 1]}
for key in all_multitask0.keys():
    all_multitask0[key][0]=1 / len(all_multitask0.keys())

class MediaCell(mesa.Agent):
    """
    A media cell.

    Attributes:
        x, y: Grid coordinates
        feature_people: pre-cause conditions.
        multitask_set: a set of multitask.
        unique_id: (x,y) tuple.

    unique_id isn't strictly necessary here, but it's good
    practice to give one to each agent anyway.
    """

    def __init__(self, feature, effect, tasking, all_multitask):
    # def __init__(self, pos, model, feature, effect, multitask, all_multitask=all_multitask0):
        """
        Create a new agent.
        Args:
            pos: The media's coordinates on the grid.
            model: standard model reference for agent.
        """

        # super().__init__(pos, model)
        # self.pos = pos
        self.feature = feature
        self.mission = tasking
        self.effect = effect
        self.all_multitask = all_multitask


    def make_choosing_decision(self):
        if self.mission.is_empty() == True:
            objective_choice = np.random.choice(list(self.all_multitask.keys()),
                                                p = np.array(list(self.all_multitask.values()))[:,0])
            self.mission.push(objective_choice, self.all_multitask[objective_choice])
        else:
            if len(list(self.mission.tasking.keys())) >= 4:
                list1 = np.array(list(self.mission.tasking.values()))[:,1]
                list1 = list(list1)
                name = list(self.mission.tasking.keys())[list1.index(max(list1))]
                del self.mission.tasking[name]
                print(self.mission.tasking)
            else:
                for key in list(self.mission.tasking.keys()):
                    if self.mission.tasking[key][1] >= 10:
                        del self.mission.tasking[key]
                        print(self.mission.tasking)
                    else:
                        objective_choice = np.random.choice(list(self.all_multitask.keys()),
                                                            p=np.array(list(self.all_multitask.values()))[:, 0])
                        self.mission.push(objective_choice, self.all_multitask[objective_choice])
            if self.effect.audio_affordance == 0:
                self.all_multitask['music'] = 0
                self.all_multitask['TV'] = 0
            elif self.effect.vision_affordance == 0:
                pass
        # self.mission.tasking[objective_choice][0] = normalization(np.array(list(self.mission.tasking.values()))[:,0])


    def effecting(self):
        for i in len(self.mission.tasking):
            if self.tasking[i] != 'music':
                self.effect.vision_affordance = 1
            elif self.tasking[i] == 'music' or 'TV':
                self.effect.audio_affordance = 1

        for i in len(self.tasking):
            if self.tasking[i] == 'reading' or 'painting':
                self.effect.enjoyment += 1
                self.effect.attention -= 5
            elif self.tasking[i] == 'music' or 'TV':
                self.effect.enjoyment += 2
                self.effect.attention -= 10
                self.effect.audio_affordance = 0
            else:
                self.effect.enjoyment += 3
                self.effect.attention -= 20
                self.effect.vision_affordance = 0

            self.value_list = list(self.tasking.values())
            self.key_list = list(self.tasking.keys())
            self.value_list = normalization(self.value_list)

            d = zip(self.key_list, self.value_list)
            self.tasking = dict(d)

    def step(self):
        """
        每次trial所做的事情厚。
        """
        MediaCell.make_choosing_decision(self)
        for key in list(self.mission.tasking.keys()):
            self.mission.tasking[key][1] += 1


def normalization(data):
    """
    归一化函数
    把所有数据归一化到[0，1]区间内，数据列表中的最大值和最小值分别映射到1和0，所以该方法一定会出现端点值0和1。
    此映射是线性映射，实质上是数据在数轴上等比缩放。

    :param data: 数据列表，数据取值范围：全体实数
    :return:
    """
    min_value = min(data)
    max_value = max(data)
    new_list = []
    if min_value - max_value == 0:
        for i in range(len(data)):
            new_list.append(1/len(data))
    else:
        for i in data:
            new_list.append((i - min_value) / (max_value - min_value))
    return new_list



class feature_people:
    """
    Represent the pre-cause of one people.
    Default attribute: age = 22, personality = ENFP, preference = music.
    """
    def __init__(self, age=22, personality='ENFP', preference='music'):
        self.age = age
        self.personality = personality
        self.preference = preference

class effect_people:
    """
    Effects that can be made and can influence decision.
    Initial state: get ability to hear, to see, energetic and feel nothing.
    """
    def __init__(self, enjoyment=0, audio_affordance=1, vision_affordance=1, attention_score=100):#exhaustion=0):
        self.enjoyment = enjoyment
        self.audio_affordance = audio_affordance
        self.vision_affordance = vision_affordance
        self.attention_score = attention_score
        # self.exhaustion = exhaustion

class mulititask_set(object):
    def __init__(self):
        """
        Represent the total tasks of one people.
        The default of number of tasks which people can handle at same time is 3.
        Value in tasking: probability, step terms, attention, enjoyment,
        audio affordance, vision affordance
        """
        self.tasking = dict()

    def push(self, task_key, task_value):
        self.tasking[task_key] = task_value

    def pop(self, delete_task):
        if self.tasking:
            return self.tasking.pop(delete_task)
        else:
            raise IndexError("There\'s no task!")

    def is_empty(self):
        # If being empty the value equals to True.
        return not bool(self.tasking)

    def size(self):
        return len(self.tasking)


a = feature_people(age=22, personality='ENFP', preference='music')
b = effect_people(enjoyment=0, audio_affordance=1, vision_affordance=1, attention_score=100)
c = mulititask_set()
d = MediaCell(a,b,c,all_multitask0)

for i in range(1, 25):
    print(i, d.mission.tasking)
    d.step()

