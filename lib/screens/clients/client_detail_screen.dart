import 'package:flutter/material.dart';
import 'package:get/get.dart';

class ClientDetailScreen extends StatefulWidget {
  const ClientDetailScreen({super.key});

  @override
  State<ClientDetailScreen> createState() => _ClientDetailScreenState();
}

class _ClientDetailScreenState extends State<ClientDetailScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('ClientDetail'),
      ),
      body: Center(
        child: Text('ClientDetail - Coming Soon'),
      ),
    );
  }
}
