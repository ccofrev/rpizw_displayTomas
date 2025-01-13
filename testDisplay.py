from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.legacy import show_message
from luma.core.legacy.font import proportional, SINCLAIR_FONT

def main():
    # Configurar el puerto SPI y el dispositivo MAX7219
    serial = spi(port=0, device=0, gpio=noop())

    # Ajustar cascaded=4 para 4 displays en serie
    device = max7219(serial, cascaded=4, block_orientation=90,
                     rotate=0, blocks_arranged_in_reverse_order=True)

    device.contrast(8)
    msg = " <3 Aswatthaama Here!!"

    while True:
        # Mostrar mensaje en todos los displays como uno solo
        show_message(device, msg, fill="red", font=proportional(SINCLAIR_FONT), scroll_delay=0.1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
