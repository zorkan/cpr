import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, ClockCycles, with_timeout

@cocotb.test()
async def test_start(dut):
    clock = Clock(dut.clk, 10, units="ns") # 40M
    cocotb.fork(clock.start())
    
    dut.RSTB <= 0
    dut.power1 <= 0;
    dut.power2 <= 0;
    dut.power3 <= 0;
    dut.power4 <= 0;

    await ClockCycles(dut.clk, 8)
    dut.power1 <= 1;
    await ClockCycles(dut.clk, 8)
    dut.power2 <= 1;
    await ClockCycles(dut.clk, 8)
    dut.power3 <= 1;
    await ClockCycles(dut.clk, 8)
    dut.power4 <= 1;

    await ClockCycles(dut.clk, 80)
    dut.RSTB <= 1
    
    await ClockCycles(dut.clk, 1180)
    dut.start <= 0
    
    await with_timeout(RisingEdge(dut.sync), 600, 'us')
    
@cocotb.test()
async def test_all(dut):
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.fork(clock.start())
    
    await ClockCycles(dut.clk, 500)   
    # Assert Output Tests
    assert dut.compress_out.value == 1
    assert dut.breath_out.value == 1
    assert dut.pulse_out.value == 1
    
    #Start system
    await ClockCycles(dut.clk, 1100)
    dut.start <= 1;
    
    await ClockCycles(dut.clk, 500)   
    # Assert Output Tests
    assert dut.compress_out.value == 0
    assert dut.breath_out.value == 0
    assert dut.pulse_out.value == 0
    
    await ClockCycles(dut.clk, 5000)
