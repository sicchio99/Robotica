import paho.mqtt.client as mqtt
from SimulatedRobot import SimulatedPioneerBody
import time

BASE_SPEED = 2.0
ANGLE_TOLERANCE = 0.02
TURN_SPEED = 0.3
SLOW_TURN_SPEED = 0.2
MORE_SLOW_TURN_SPEED = 0.1


class Body:
    _actuators: list
    # _motions: list
    _sim_body: SimulatedPioneerBody
    _go: bool

    # _orientation: float

    def __init__(self, actuators):
        assert isinstance(actuators, list)
        # self._motions = motions
        self._actuators = actuators
        self._sim_body = SimulatedPioneerBody("PioneerP3DX")
        self._sim_body.start()
        self._go = False
        # self._orientation = 0.0

    def exists_actuator(self, name):
        return name in self._actuators

    def do_action(self, actuator, value):
        print(f"Executing action on actuator {actuator} with value {value}")
        self._sim_body.do_action(actuator, value)

    def set_speeds(self, left_speed, right_speed):
        print(f"Setting speeds: right = {right_speed}, left = {left_speed}")
        self.do_action("leftMotor", left_speed)
        self.do_action("rightMotor", right_speed)

    def go_straight(self):
        self.set_speeds(BASE_SPEED, BASE_SPEED)
        # self._go = True

    def turn_left(self, vel):
        self.set_speeds(-vel, vel)

    def turn_right(self, vel):
        self.set_speeds(vel, -vel)


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print(
            f"Failed to connect: {reason_code}. loop_forever() will retry connection")
    else:
        client.subscribe("controller/#")


def on_message(client, userdata, msg):
    name = msg.topic.split("/")[1]
    value = msg.payload.decode("utf-8")
    # print(name, value)

    if name == "direction":
        # if value == "go" and not my_robot._go:
        if value == "rotation_done":
            print("Rotation done")
            client_mqtt.disconnect()
            my_robot.go_straight()
            time.sleep(2.5)
            client_mqtt.reconnect()
            # my_robot.set_speeds(BASE_SPEED, BASE_SPEED)
            # my_robot._go = True
            print("Velocità base")
        # elif value == "cross" and my_robot._go:
        elif value == "go" or "front":
            print("go")
            my_robot.go_straight()
        elif value == "cross":
            print("CROSS")
            my_robot.set_speeds(0, 0)
        elif value == "turn_left":
            print("turn_left")
            my_robot.turn_left(TURN_SPEED)
        elif value == "turn_left_slow":
            print("turn_left_slow")
            my_robot.turn_left(SLOW_TURN_SPEED)
        elif value == "turn_left_more_slow":
            print("turn_left_more_slow")
            my_robot.turn_left(MORE_SLOW_TURN_SPEED)
        elif value == "turn_right":
            print("turn_right")
            my_robot.turn_right(TURN_SPEED)
        elif value == "turn_right_slow":
            print("turn_right_slow")
            my_robot.turn_right(SLOW_TURN_SPEED)
        elif value == "turn_right_more_slow":
            print("turn_right_more_slow")
            my_robot.turn_right(MORE_SLOW_TURN_SPEED)
        elif value == "stop":
            print("Stop")
            time.sleep(30)
        else:
            print("Invalid")
            my_robot.set_speeds(0, 0)

    client.publish("action", value, my_robot._go)


def on_subscribe(client, userdata, mid, reason_code_list, properties):
    if reason_code_list[0].is_failure:
        print(f"Broker rejected you subscription: {reason_code_list[0]}")
    else:
        client.subscribe("controls/#")


if __name__ == "__main__":
    my_robot = Body(["leftMotor", "rightMotor"])

    client_mqtt = mqtt.Client(
        mqtt.CallbackAPIVersion.VERSION2, reconnect_on_failure=True)
    client_mqtt.connect("mosquitto", 1883)
    client_mqtt.on_connect = on_connect
    client_mqtt.on_message = on_message
    client_mqtt.on_subscribe = on_subscribe
    client_mqtt.loop_forever()
