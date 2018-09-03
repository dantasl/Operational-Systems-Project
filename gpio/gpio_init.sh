export_dir=/sys/class/gpio/export
gpio_dir=/sys/class/gpio/gpio

led_vermelho=50
led_amarelo=2
led_verde=112
botao=115

initButton() {
	echo $1 > $export_dir
	echo $1 exported

	echo in > $gpio_dir$1/direction
	cat $gpio_dir$1/direction
}

initLed() {
	echo $1 > $export_dir
	echo $1 exported

	echo out > $gpio_dir$1/direction
	cat $gpio_dir$1/direction

	echo 0 > $gpio_dir$1/value
	cat $gpio_dir$1/value
}

initLed $led_vermelho
initLed $led_amarelo
initLed $led_verde