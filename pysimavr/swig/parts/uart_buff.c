/*
 uart_buff.c

 Copyright 2008, 2009 Michel Pollet <buserror@gmail.com>

 This file is part of simavr.

 simavr is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 simavr is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with simavr.  If not, see <http://www.gnu.org/licenses/>.
 */

#include <pthread.h>
#include <string.h>
#include <stdio.h>
#include <errno.h>
#include <unistd.h>

#include "uart_buff.h"
#include "avr_uart.h"
#include "sim_hex.h"

DEFINE_FIFO(uint8_t, uart_buff_fifo);

/*
 * called when a byte is send via the uart on the AVR
 */
static void uart_buff_in_hook(struct avr_irq_t * irq, uint32_t value,
        void * param)
{
    uart_buff_t * p = (uart_buff_t*) param;
//	printf("uart_buff_in_hook %02x\n", value);
    uart_buff_fifo_write(&p->fifo_in, value);
}

/*
 * Called when the uart has room in it's input buffer. This is called repeateadly
 * if necessary, while the xoff is called only when the uart fifo is FULL
 */
static void uart_buff_xon_hook(struct avr_irq_t * irq, uint32_t value,
        void * param)
{
    uart_buff_t * p = (uart_buff_t*) param;
//	if (!p->xon)
//		printf("uart_buff_xon_hook\n");
    p->xon = 1;
    // try to empty our fifo, the uart_buff_xoff_hook() will be called when
    // other side is full
    while (p->xon && !uart_buff_fifo_isempty(&p->fifo_out))
    {
        uint8_t byte = uart_buff_fifo_read(&p->fifo_out);
        //	printf("uart_buff_xon_hook send %02x\n", byte);
        avr_raise_irq(p->irq + IRQ_uart_buff_BYTE_OUT, byte);
    }
}

/*
 * Called when the uart ran out of room in it's input buffer
 */
static void uart_buff_xoff_hook(struct avr_irq_t * irq, uint32_t value,
        void * param)
{
    uart_buff_t * p = (uart_buff_t*) param;
//	if (p->xon)
//		printf("uart_buff_xoff_hook\n");
    p->xon = 0;
}

static void * uart_buff_thread(void * param)
{
//	uart_buff_t * p = (uart_buff_t*)param;
//
//	while (!p->_terminate) {
//		fd_set read_set, write_set;
//		int max = p->s + 1;
//		FD_ZERO(&read_set);
//		FD_ZERO(&write_set);
//
//		FD_SET(p->s, &read_set);
//		if (!uart_buff_fifo_isempty(&p->fifo_in))
//			FD_SET(p->s, &write_set);
//
//		struct timeval timo = { 0, 500 };	// short, but not too short interval
//		int ret = select(max, &read_set, &write_set, NULL, &timo);
//
//		if (!ret)
//			continue;
//
//		if (FD_ISSET(p->s, &read_set)) {
//			uint8_t buffer[512];
//
//			socklen_t len = sizeof(p->peer);
//			ssize_t r = recvfrom(p->s, buffer, sizeof(buffer)-1, 0, (struct sockaddr*)&p->peer, &len);
//
//		//	hdump("udp recv", buffer, r);
//
//			// write them in fifo
//			uint8_t * src = buffer;
//			while (r-- && !uart_buff_fifo_isfull(&p->fifo_out))
//				uart_buff_fifo_write(&p->fifo_out, *src++);
//			if (r > 0)
//				printf("UDP dropped %zu bytes\n", r);
//		}
//		if (FD_ISSET(p->s, &write_set)) {
//			uint8_t buffer[512];
//			// write them in fifo
//			uint8_t * dst = buffer;
//			while (!uart_buff_fifo_isempty(&p->fifo_in) && dst < (buffer+sizeof(buffer)))
//				*dst++ = uart_buff_fifo_read(&p->fifo_in);
//			socklen_t len = dst - buffer;
//			/*size_t r = */sendto(p->s, buffer, len, 0, (struct sockaddr*)&p->peer, sizeof(p->peer));
//		//	hdump("udp send", buffer, r);
//		}
//	}
    return NULL;
}

static const char * irq_names[IRQ_uart_buff_COUNT] =
{ [IRQ_uart_buff_BYTE_IN] = "8<uart_buff.fifo_in", [IRQ_uart_buff_BYTE_OUT
        ] = "8>uart_buff.fifo_out", };

void uart_buff_init(struct avr_t * avr, uart_buff_t * p)
{
    p->avr = avr;
    p->irq = avr_alloc_irq(&avr->irq_pool, 0, IRQ_uart_buff_COUNT, irq_names);
    avr_irq_register_notify(p->irq + IRQ_uart_buff_BYTE_IN, uart_buff_in_hook,
            p);

//	if ((p->s = socket(PF_INET, SOCK_DGRAM, 0)) < 0) {
//		fprintf(stderr, "%s: Can't create socket: %s", __FUNCTION__, strerror(errno));
//		return ;
//	}

//	struct sockaddr_in address = { 0 };
//	address.sin_family = AF_INET;
//	address.sin_port = htons (4321);

//	if (bind(p->s, (struct sockaddr *) &address, sizeof(address))) {
//		fprintf(stderr, "%s: Can not bind socket: %s", __FUNCTION__, strerror(errno));
//		return ;
//	}

//	printf("uart_buff_init bridge on port %d\n", 4321);

//	pthread_create(&p->thread, NULL, uart_buff_thread, p);

}

void uart_buff_terminate(uart_buff_t * p)
{
//	p->_terminate=1;
//	pthread_join(p->thread, NULL);
//	close(p->s);
//	shutdown(p->s,SHUT_RDWR);
}

void uart_buff_connect(uart_buff_t * p, char uart)
{
    // disable the stdio dump, as we are sending binary there
//	uint32_t f = 0;
//	avr_ioctl(p->avr, AVR_IOCTL_UART_GET_FLAGS(uart), &f);
//	f &= ~AVR_UART_FLAG_STDIO;
//	avr_ioctl(p->avr, AVR_IOCTL_UART_SET_FLAGS(uart), &f);

    avr_irq_t * src = avr_io_getirq(p->avr, AVR_IOCTL_UART_GETIRQ(uart),
            UART_IRQ_OUTPUT);
    avr_irq_t * dst = avr_io_getirq(p->avr, AVR_IOCTL_UART_GETIRQ(uart),
            UART_IRQ_INPUT);
    avr_irq_t * xon = avr_io_getirq(p->avr, AVR_IOCTL_UART_GETIRQ(uart),
            UART_IRQ_OUT_XON);
    avr_irq_t * xoff = avr_io_getirq(p->avr, AVR_IOCTL_UART_GETIRQ(uart),
            UART_IRQ_OUT_XOFF);
    if (src && dst)
    {
        avr_connect_irq(src, p->irq + IRQ_uart_buff_BYTE_IN);
        avr_connect_irq(p->irq + IRQ_uart_buff_BYTE_OUT, dst);
    }
    if (xon)
        avr_irq_register_notify(xon, uart_buff_xon_hook, p);
    if (xoff)
        avr_irq_register_notify(xoff, uart_buff_xoff_hook, p);
}

int read_fifo(uart_buff_fifo_t* fifo)
{
    if (uart_buff_fifo_isempty(fifo))
        return -1;
    return uart_buff_fifo_read(fifo);
}

int write_fifo(uart_buff_fifo_t* fifo, uint8_t c)
{
    if (uart_buff_fifo_isfull(fifo))
        return -1;
    uart_buff_fifo_write(fifo, c);
    return 0;
}
