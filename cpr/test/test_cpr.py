import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, ClockCycles
import random


async def reset(dut):
    dut.start <= 0;
    await ClockCycles(dut.clk, 5)
    dut.rst  <= 1
    await ClockCycles(dut.clk, 5)
    dut.rst <= 0;
    await ClockCycles(dut.clk, 5) # how long to wait for the debouncers to clear

@cocotb.test()
async def test_all(dut):
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.fork(clock.start())

    # pwm should all be low at start
    assert dut.breath_out == 0
    assert dut.compress_out == 0
    assert dut.pulse_out == 0
    
    await reset(dut)
    
    await ClockCycles(dut.clk, 100)
    
    # pwm should all be low at start
    assert dut.breath_out == 1
    assert dut.compress_out == 1
    assert dut.pulse_out == 1

    await ClockCycles(dut.clk, 1000)
    dut.start <= 1;
    await ClockCycles(dut.clk, 2000)
    dut.rst <= 1;
    await ClockCycles(dut.clk, 1000)
    dut.rst <= 0;
    await ClockCycles(dut.clk, 5000)
    dut.rst <= 1;
    await ClockCycles(dut.clk, 400)
    dut.rst <= 0;
    await ClockCycles(dut.clk, 15000)
    dut.start <= 0;
    await ClockCycles(dut.clk, 3000)
    dut.start <= 1;
    await ClockCycles(dut.clk, 3000)
