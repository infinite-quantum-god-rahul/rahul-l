import 'package:flutter/material.dart';
import 'package:get/get.dart';

class ClientListScreen extends StatefulWidget {
  const ClientListScreen({super.key});

  @override
  State<ClientListScreen> createState() => _ClientListScreenState();
}

class _ClientListScreenState extends State<ClientListScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('ClientList'),
      ),
      body: Center(
        child: Text('ClientList - Coming Soon'),
      ),
    );
  }
}
