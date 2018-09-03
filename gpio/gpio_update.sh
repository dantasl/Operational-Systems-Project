gpio_dir=/sys/class/gpio/gpio

led_vermelho=50
led_amarelo=2
led_verde=112
botao=115

updateLed() {
	echo $2 > $gpio_dir$1/value
	echo $1 to $2
}

updateLed $led_vermelho 1