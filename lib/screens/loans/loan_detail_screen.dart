import 'package:flutter/material.dart';
import 'package:get/get.dart';

class LoanDetailScreen extends StatefulWidget {
  const LoanDetailScreen({super.key});

  @override
  State<LoanDetailScreen> createState() => _LoanDetailScreenState();
}

class _LoanDetailScreenState extends State<LoanDetailScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('LoanDetail'),
      ),
      body: Center(
        child: Text('LoanDetail - Coming Soon'),
      ),
    );
  }
}
