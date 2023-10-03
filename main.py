from basicClient import BasicPikaClient

class BasicMessageReceiver(BasicPikaClient):

    def get_message(self, queue):
        method_frame, header_frame, body = self.channel.basic_get(queue)
        if method_frame:
            print(method_frame, header_frame, body)
            self.channel.basic_ack(method_frame.delivery_tag)
            return method_frame, header_frame, body
        else:
            print('No message returned')

    def close(self):
        self.channel.close()
        self.connection.close()


if __name__ == "__main__":

    # Create Basic Message Receiver which creates a connection
    # and channel for consuming messages.
    basic_message_receiver = BasicMessageReceiver(
        "localhost",
        "<EXAMPLE>",
        "<EXAMPLE>",
        "<PORT>"
    )

    # Consume the message that was sent.
    basic_message_receiver.get_message("maker-iot-new-topic-queue")

    # Close connections.
    basic_message_receiver.close()
