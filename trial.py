import random
from direct.showbase.ShowBase import ShowBase
from direct.task import Task


class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        self.lanes = [[] for _ in range(3)]

        # Load the environment model.
        self.scene = self.loader.loadModel("models/environment")

        # Reparent the model to render.
        self.scene.reparentTo(self.render)

        # Apply scale and position transforms on the model.
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, -1)

        self.car_y = 0
        self.zoom = 1.2

        self.taskMgr.add(self.moveCameraTask, "moveCamera")
        self.taskMgr.doMethodLater(2, self.next_car, "add car task")

        self.add_car()

    def add_car(self):
        car = self.loader.loadModel("truck.egg")
        car.reparentTo(self.render)
        car.setHpr(180, 0, 0)
        lane = random.choice(range(3))
        car.setPos(5 * lane, self.car_y - (8 * len(self.lanes[lane]) + 50), 0)
        self.lanes[lane].append(car)

    def run(self):
        super().run()

    def moveCameraTask(self, task):
        self.car_y += 0.01
        for laneno, lane in enumerate(self.lanes):
            for i, car in enumerate(lane):
                target_y = self.car_y - (8 * i) + 2 * (hash((i * 997, laneno)) % 100 / 99)
                _, y, _ = car.getPos()
                car.setPos(5 * laneno, y * 0.97 + target_y * 0.03, 0)
        self.camera.setPos(10 * self.zoom, self.car_y - 10 * self.zoom * 1.3, 15 * self.zoom)
        self.camera.setHpr(45, -45, 0)
        self.zoom += 0.01 * 0.3
        return Task.cont

    def next_car(self, task):
        self.add_car()
        task.delayTime = 2
        return task.again

if __name__ == '__main__':
    app = MyApp()
    app.run()
