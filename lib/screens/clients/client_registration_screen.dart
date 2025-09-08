import 'package:flutter/material.dart';
import 'package:get/get.dart';

class ClientRegistrationScreen extends StatefulWidget {
  const ClientRegistrationScreen({super.key});

  @override
  State<ClientRegistrationScreen> createState() => _ClientRegistrationScreenState();
}

class _ClientRegistrationScreenState extends State<ClientRegistrationScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('ClientRegistration'),
      ),
      body: Center(
        child: Text('ClientRegistration - Coming Soon'),
      ),
    );
  }
}
