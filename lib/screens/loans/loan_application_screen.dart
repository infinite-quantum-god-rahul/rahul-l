import 'package:flutter/material.dart';
import 'package:get/get.dart';

class LoanApplicationScreen extends StatefulWidget {
  const LoanApplicationScreen({super.key});

  @override
  State<LoanApplicationScreen> createState() => _LoanApplicationScreenState();
}

class _LoanApplicationScreenState extends State<LoanApplicationScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('LoanApplication'),
      ),
      body: Center(
        child: Text('LoanApplication - Coming Soon'),
      ),
    );
  }
}
