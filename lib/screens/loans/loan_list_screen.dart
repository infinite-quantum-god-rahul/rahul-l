import 'package:flutter/material.dart';
import 'package:get/get.dart';

class LoanListScreen extends StatefulWidget {
  const LoanListScreen({super.key});

  @override
  State<LoanListScreen> createState() => _LoanListScreenState();
}

class _LoanListScreenState extends State<LoanListScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('LoanList'),
      ),
      body: Center(
        child: Text('LoanList - Coming Soon'),
      ),
    );
  }
}
