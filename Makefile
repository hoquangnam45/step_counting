CC=g++
CFLAGS=-g -c -Wall -std=c++11
LDFLAGS=-lmraa
SOURCES=step_counting.cpp Libs/Gyro/SFE_LSM9DS0.cpp Libs/OLED/gpio/gpio_edison.cpp Libs/OLED/oled/Edison_OLED.cpp Libs/OLED/spi/spi_device_edison.cpp Libs/OLED/spi/spi_port_edison.cpp
OBJECTS=$(SOURCES:.cpp=.o)
EXECUTABLE=step_counting

all: $(SOURCES) $(EXECUTABLE)

$(EXECUTABLE): $(OBJECTS) 
	$(CC) -g $(OBJECTS) -o $@ $(LDFLAGS)

.cpp.o:
	$(CC) $(CFLAGS) $< -o $@

clean:
	rm -rf *.o $(EXECUTABLE)
	find . -type f -name '*.o' -exec rm {} +
