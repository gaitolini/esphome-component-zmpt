import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor, voltage_sampler
from esphome.const import (
    CONF_SENSOR,
    DEVICE_CLASS_VOLTAGE,
    STATE_CLASS_MEASUREMENT,
    UNIT_VOLT,
)

AUTO_LOAD = ["voltage_sampler"]
CODEOWNERS = ["@gaitolini"]

CONF_SAMPLE_DURATION = "sample_duration"

voltage_ns = cg.esphome_ns.namespace("voltage")
VoltageSensor = voltage_ns.class_("VoltageSensor", sensor.Sensor, cg.PollingComponent)

CONFIG_SCHEMA = (
    sensor.sensor_schema(
        VoltageSensor,
        unit_of_measurement=UNIT_VOLT,
        accuracy_decimals=2,
        device_class=DEVICE_CLASS_VOLTAGE,
        state_class=STATE_CLASS_MEASUREMENT,
    )
    .extend(
        {
            cv.Required(CONF_SENSOR): cv.use_id(voltage_sampler.VoltageSampler),
            cv.Optional(
                CONF_SAMPLE_DURATION, default="200ms"
            ): cv.positive_time_period_milliseconds,
        }
    )
    .extend(cv.polling_component_schema("60s"))
)

async def to_code(config):
    var = await sensor.new_sensor(config)
    await cg.register_component(var, config)

    sens = await cg.get_variable(config[CONF_SENSOR])
    cg.add(var.set_source(sens))
    cg.add(var.set_sample_duration(config[CONF_SAMPLE_DURATION]))
