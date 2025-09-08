import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:qr_flutter/qr_flutter.dart';
import 'package:mobile_scanner/mobile_scanner.dart';
import 'package:image_picker/image_picker.dart';
import 'package:file_picker/file_picker.dart';
import 'package:path/path.dart' as path;

import '../../config/app_theme.dart';
import '../../models/sml_models.dart';
import '../../widgets/common/custom_button.dart';
import '../../widgets/common/custom_text_field.dart';
import '../../widgets/common/loading_overlay.dart';
import '../../utils/constants.dart';

class QRDocumentManagementScreen extends StatefulWidget {
  const QRDocumentManagementScreen({Key? key}) : super(key: key);

  @override
  State<QRDocumentManagementScreen> createState() => _QRDocumentManagementScreenState();
}

class _QRDocumentManagementScreenState extends State<QRDocumentManagementScreen>
    with TickerProviderStateMixin {
  late AnimationController _animationController;
  late Animation<double> _fadeAnimation;
  late Animation<Offset> _slideAnimation;

  final TextEditingController _searchController = TextEditingController();
  final TextEditingController _documentNameController = TextEditingController();
  final TextEditingController _documentNumberController = TextEditingController();

  String _selectedDocumentType = 'aadhaar';
  String _selectedStatus = 'pending';
  bool _isScanning = false;
  String? _scannedData;
  List<Map<String, dynamic>> _documents = [];

  @override
  void initState() {
    super.initState();
    _initializeAnimations();
    _loadSampleDocuments();
  }

  void _initializeAnimations() {
    _animationController = AnimationController(
      duration: const Duration(milliseconds: 800),
      vsync: this,
    );

    _fadeAnimation = Tween<double>(
      begin: 0.0,
      end: 1.0,
    ).animate(CurvedAnimation(
      parent: _animationController,
      curve: Curves.easeInOut,
    ));

    _slideAnimation = Tween<Offset>(
      begin: const Offset(0, 0.3),
      end: Offset.zero,
    ).animate(CurvedAnimation(
      parent: _animationController,
      curve: Curves.easeOutCubic,
    ));

    _animationController.forward();
  }

  void _loadSampleDocuments() {
    _documents = [
      {
        'id': 1,
        'name': 'Aadhaar Card',
        'number': '1234-5678-9012',
        'type': 'aadhaar',
        'status': 'verified',
        'uploadDate': '2024-01-15',
        'expiryDate': '2034-01-15',
        'fileSize': '2.5 MB',
        'fileName': 'aadhaar_card.pdf',
      },
      {
        'id': 2,
        'name': 'PAN Card',
        'number': 'ABCDE1234F',
        'type': 'pan',
        'status': 'pending',
        'uploadDate': '2024-01-10',
        'expiryDate': '2029-01-10',
        'fileSize': '1.8 MB',
        'fileName': 'pan_card.pdf',
      },
      {
        'id': 3,
        'name': 'Bank Statement',
        'number': 'SB123456789',
        'type': 'bank_statement',
        'status': 'verified',
        'uploadDate': '2024-01-05',
        'expiryDate': '2024-12-31',
        'fileSize': '3.2 MB',
        'fileName': 'bank_statement.pdf',
      },
    ];
  }

  @override
  void dispose() {
    _animationController.dispose();
    _searchController.dispose();
    _documentNameController.dispose();
    _documentNumberController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      length: 4,
      child: Scaffold(
        body: LoadingOverlay(
          isLoading: false,
          child: Column(
            children: [
              _buildTabBar(),
              Expanded(
                child: TabBarView(
                  children: [
                    _buildQRScannerTab(),
                    _buildDocumentUploadTab(),
                    _buildKYCDocumentsTab(),
                    _buildDigitalSignatureTab(),
                  ],
                ),
              ),
            ],
          ),
        ),
        floatingActionButton: _buildFloatingActionButton(),
      ),
    );
  }

  Widget _buildTabBar() {
    return Container(
      color: AppTheme.primaryColor,
      child: TabBar(
        labelColor: Colors.white,
        unselectedLabelColor: Colors.white70,
        indicatorColor: Colors.white,
        isScrollable: true,
        tabs: const [
          Tab(icon: Icon(Icons.qr_code_scanner), text: 'QR Scanner'),
          Tab(icon: Icon(Icons.upload_file), text: 'Upload'),
          Tab(icon: Icon(Icons.verified_user), text: 'KYC'),
          Tab(icon: Icon(Icons.draw), text: 'Signature'),
        ],
      ),
    );
  }

  Widget _buildQRScannerTab() {
    return CustomScrollView(
      slivers: [
        _buildQRScannerHeader(),
        _buildQRScannerContent(),
        _buildScannedDataDisplay(),
      ],
    );
  }

  Widget _buildDocumentUploadTab() {
    return CustomScrollView(
      slivers: [
        _buildDocumentUploadHeader(),
        _buildUploadForm(),
        _buildUploadedDocuments(),
      ],
    );
  }

  Widget _buildKYCDocumentsTab() {
    return CustomScrollView(
      slivers: [
        _buildKYCDocumentsHeader(),
        _buildKYCDocumentsList(),
      ],
    );
  }

  Widget _buildDigitalSignatureTab() {
    return CustomScrollView(
      slivers: [
        _buildDigitalSignatureHeader(),
        _buildSignatureCanvas(),
        _buildSignatureOptions(),
      ],
    );
  }

  Widget _buildQRScannerHeader() {
    return SliverAppBar(
      expandedHeight: 120,
      floating: false,
      pinned: true,
      backgroundColor: AppTheme.primaryColor,
      flexibleSpace: FlexibleSpaceBar(
        title: const Text('QR Scanner', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
        background: Container(
          decoration: BoxDecoration(gradient: AppTheme.primaryGradient),
          child: Padding(
            padding: const EdgeInsets.fromLTRB(16, 60, 16, 16),
            child: Row(
              children: [
                Expanded(child: _buildQuickStat('Scanned', '0', Icons.qr_code_scanner)),
                Expanded(child: _buildQuickStat('Valid', '0', Icons.check_circle)),
                Expanded(child: _buildQuickStat('Invalid', '0', Icons.error)),
                Expanded(child: _buildQuickStat('History', '0', Icons.history)),
              ],
            ),
          ),
        ),
      ),
      actions: [
        IconButton(icon: const Icon(Icons.history, color: Colors.white), onPressed: _showScanHistory),
        IconButton(icon: const Icon(Icons.settings, color: Colors.white), onPressed: _showScannerSettings),
      ],
    );
  }

  Widget _buildDocumentUploadHeader() {
    return SliverAppBar(
      expandedHeight: 120,
      floating: false,
      pinned: true,
      backgroundColor: AppTheme.secondaryColor,
      flexibleSpace: FlexibleSpaceBar(
        title: const Text('Document Upload', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
        background: Container(
          decoration: BoxDecoration(gradient: AppTheme.successGradient),
          child: Padding(
            padding: const EdgeInsets.fromLTRB(16, 60, 16, 16),
            child: Row(
              children: [
                Expanded(child: _buildQuickStat('Uploaded', '0', Icons.upload_file)),
                Expanded(child: _buildQuickStat('Pending', '0', Icons.pending)),
                Expanded(child: _buildQuickStat('Verified', '0', Icons.verified)),
                Expanded(child: _buildQuickStat('Rejected', '0', Icons.cancel)),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildKYCDocumentsHeader() {
    return SliverAppBar(
      expandedHeight: 120,
      floating: false,
      pinned: true,
      backgroundColor: AppTheme.accentColor,
      flexibleSpace: FlexibleSpaceBar(
        title: const Text('KYC Documents', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
        background: Container(
          decoration: BoxDecoration(gradient: AppTheme.warningGradient),
          child: Padding(
            padding: const EdgeInsets.fromLTRB(16, 60, 16, 16),
            child: Row(
              children: [
                Expanded(child: _buildQuickStat('Total', '0', Icons.description)),
                Expanded(child: _buildQuickStat('Complete', '0', Icons.check_circle)),
                Expanded(child: _buildQuickStat('Incomplete', '0', Icons.pending)),
                Expanded(child: _buildQuickStat('Expired', '0', Icons.warning)),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildDigitalSignatureHeader() {
    return SliverAppBar(
      expandedHeight: 120,
      floating: false,
      pinned: true,
      backgroundColor: AppTheme.infoColor,
      flexibleSpace: FlexibleSpaceBar(
        title: const Text('Digital Signature', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
        background: Container(
          decoration: BoxDecoration(gradient: AppTheme.infoGradient),
          child: Padding(
            padding: const EdgeInsets.fromLTRB(16, 60, 16, 16),
            child: Row(
              children: [
                Expanded(child: _buildQuickStat('Signed', '0', Icons.draw)),
                Expanded(child: _buildQuickStat('Pending', '0', Icons.pending)),
                Expanded(child: _buildQuickStat('Templates', '5', Icons.template)),
                Expanded(child: _buildQuickStat('History', '0', Icons.history)),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildQuickStat(String label, String value, IconData icon) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Icon(icon, color: Colors.white70, size: 20),
        const SizedBox(height: 4),
        Text(value, style: const TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold)),
        Text(label, style: const TextStyle(color: Colors.white70, fontSize: 12)),
      ],
    );
  }

  Widget _buildQRScannerContent() {
    return SliverToBoxAdapter(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('QR Code Scanner', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),
            _buildScannerContainer(),
            const SizedBox(height: 16),
            _buildScannerControls(),
          ],
        ),
      ),
    );
  }

  Widget _buildScannerContainer() {
    return Container(
      height: 300,
      decoration: BoxDecoration(
        border: Border.all(color: AppTheme.primaryColor, width: 2),
        borderRadius: BorderRadius.circular(12),
      ),
      child: ClipRRect(
        borderRadius: BorderRadius.circular(10),
        child: _isScanning
            ? MobileScanner(
                onDetect: (capture) {
                  final List<Barcode> barcodes = capture.barcodes;
                  for (final barcode in barcodes) {
                    setState(() {
                      _scannedData = barcode.rawValue;
                      _isScanning = false;
                    });
                    _processScannedData(barcode.rawValue ?? '');
                  }
                },
              )
            : Container(
                color: Colors.grey[200],
                child: Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(Icons.qr_code_scanner, size: 80, color: Colors.grey[400]),
                      const SizedBox(height: 16),
                      Text('Scanner Ready', style: TextStyle(fontSize: 18, color: Colors.grey[600])),
                      const SizedBox(height: 8),
                      Text('Tap Start to begin scanning', style: TextStyle(fontSize: 14, color: Colors.grey[500])),
                    ],
                  ),
                ),
              ),
      ),
    );
  }

  Widget _buildScannerControls() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
      children: [
        CustomButton(
          text: _isScanning ? 'Stop' : 'Start',
          onPressed: _toggleScanner,
          icon: _isScanning ? Icons.stop : Icons.play_arrow,
          style: _isScanning ? CustomButtonStyle.danger : CustomButtonStyle.primary,
        ),
        CustomButton(
          text: 'Flash',
          onPressed: _toggleFlash,
          icon: Icons.flash_on,
          style: CustomButtonStyle.secondary,
        ),
        CustomButton(
          text: 'Gallery',
          onPressed: _scanFromGallery,
          icon: Icons.photo_library,
          style: CustomButtonStyle.info,
        ),
      ],
    );
  }

  Widget _buildScannedDataDisplay() {
    if (_scannedData == null) {
      return const SliverToBoxAdapter(child: SizedBox.shrink());
    }

    return SliverToBoxAdapter(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Scanned Data', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),
            Card(
              elevation: 4,
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Icon(Icons.qr_code, color: AppTheme.primaryColor, size: 24),
                        const SizedBox(width: 12),
                        Expanded(
                          child: Text(
                            _scannedData!,
                            style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
                          ),
                        ),
                        IconButton(
                          onPressed: _copyScannedData,
                          icon: const Icon(Icons.copy),
                          color: AppTheme.primaryColor,
                        ),
                      ],
                    ),
                    const SizedBox(height: 16),
                    Row(
                      children: [
                        Expanded(
                          child: CustomButton(
                            text: 'Process',
                            onPressed: () => _processScannedData(_scannedData!),
                            icon: Icons.check,
                            style: CustomButtonStyle.success,
                          ),
                        ),
                        const SizedBox(width: 12),
                        Expanded(
                          child: CustomButton(
                            text: 'Clear',
                            onPressed: _clearScannedData,
                            icon: Icons.clear,
                            style: CustomButtonStyle.danger,
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildUploadForm() {
    return SliverToBoxAdapter(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Upload Document', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),
            Card(
              elevation: 4,
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  children: [
                    _buildDocumentTypeDropdown(),
                    const SizedBox(height: 16),
                    _buildDocumentNameField(),
                    const SizedBox(height: 16),
                    _buildDocumentNumberField(),
                    const SizedBox(height: 16),
                    _buildFileUploadSection(),
                    const SizedBox(height: 16),
                    _buildUploadButton(),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildDocumentTypeDropdown() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text('Document Type', style: TextStyle(fontSize: 14, fontWeight: FontWeight.w600)),
        const SizedBox(height: 8),
        DropdownButtonFormField<String>(
          value: _selectedDocumentType,
          decoration: InputDecoration(
            border: OutlineInputBorder(borderRadius: BorderRadius.circular(8)),
            contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
          ),
          items: [
            DropdownMenuItem(value: 'aadhaar', child: Text('Aadhaar Card')),
            DropdownMenuItem(value: 'pan', child: Text('PAN Card')),
            DropdownMenuItem(value: 'passport', child: Text('Passport')),
            DropdownMenuItem(value: 'driving_license', child: Text('Driving License')),
            DropdownMenuItem(value: 'bank_statement', child: Text('Bank Statement')),
            DropdownMenuItem(value: 'salary_slip', child: Text('Salary Slip')),
            DropdownMenuItem(value: 'utility_bill', child: Text('Utility Bill')),
            DropdownMenuItem(value: 'other', child: Text('Other')),
          ],
          onChanged: (value) => setState(() => _selectedDocumentType = value!),
        ),
      ],
    );
  }

  Widget _buildDocumentNameField() {
    return CustomTextField(
      controller: _documentNameController,
      labelText: 'Document Name',
      hintText: 'Enter document name',
      prefixIcon: Icons.description,
    );
  }

  Widget _buildDocumentNumberField() {
    return CustomTextField(
      controller: _documentNumberController,
      labelText: 'Document Number',
      hintText: 'Enter document number',
      prefixIcon: Icons.numbers,
    );
  }

  Widget _buildFileUploadSection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text('File Upload', style: TextStyle(fontSize: 14, fontWeight: FontWeight.w600)),
        const SizedBox(height: 8),
        Row(
          children: [
            Expanded(
              child: CustomButton(
                text: 'Camera',
                onPressed: _captureFromCamera,
                icon: Icons.camera_alt,
                style: CustomButtonStyle.primary,
              ),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: CustomButton(
                text: 'Gallery',
                onPressed: _pickFromGallery,
                icon: Icons.photo_library,
                style: CustomButtonStyle.secondary,
              ),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: CustomButton(
                text: 'Files',
                onPressed: _pickFromFiles,
                icon: Icons.folder_open,
                style: CustomButtonStyle.info,
              ),
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildUploadButton() {
    return SizedBox(
      width: double.infinity,
      child: CustomButton(
        text: 'Upload Document',
        onPressed: _uploadDocument,
        icon: Icons.upload,
        style: CustomButtonStyle.success,
      ),
    );
  }

  Widget _buildUploadedDocuments() {
    return SliverToBoxAdapter(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Uploaded Documents', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),
            ListView.builder(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              itemCount: _documents.length,
              itemBuilder: (context, index) {
                final document = _documents[index];
                return _buildDocumentCard(document);
              },
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildDocumentCard(Map<String, dynamic> document) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      elevation: 3,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: ListTile(
        leading: CircleAvatar(
          backgroundColor: _getDocumentTypeColor(document['type']).withOpacity(0.1),
          child: Icon(_getDocumentTypeIcon(document['type']), color: _getDocumentTypeColor(document['type'])),
        ),
        title: Text(document['name'], style: const TextStyle(fontWeight: FontWeight.w600)),
        subtitle: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Number: ${document['number']}'),
            Text('Status: ${document['status'].toString().toUpperCase()}'),
            Text('Uploaded: ${document['uploadDate']}'),
          ],
        ),
        trailing: PopupMenuButton(
          itemBuilder: (context) => [
            const PopupMenuItem(value: 'view', child: Text('View')),
            const PopupMenuItem(value: 'download', child: Text('Download')),
            const PopupMenuItem(value: 'verify', child: Text('Verify')),
            const PopupMenuItem(value: 'delete', child: Text('Delete')),
          ],
          onSelected: (value) => _handleDocumentAction(value, document),
        ),
      ),
    );
  }

  Widget _buildKYCDocumentsList() {
    return SliverToBoxAdapter(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('KYC Documents', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),
            _buildKYCDocumentItem('Aadhaar Card', 'Required', 'verified', Icons.credit_card),
            const SizedBox(height: 8),
            _buildKYCDocumentItem('PAN Card', 'Required', 'pending', Icons.credit_card),
            const SizedBox(height: 8),
            _buildKYCDocumentItem('Bank Statement', 'Required', 'verified', Icons.account_balance),
            const SizedBox(height: 8),
            _buildKYCDocumentItem('Address Proof', 'Required', 'missing', Icons.location_on),
            const SizedBox(height: 8),
            _buildKYCDocumentItem('Income Proof', 'Required', 'pending', Icons.attach_money),
            const SizedBox(height: 8),
            _buildKYCDocumentItem('Photo', 'Required', 'verified', Icons.face),
          ],
        ),
      ),
    );
  }

  Widget _buildKYCDocumentItem(String name, String requirement, String status, IconData icon) {
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
      child: ListTile(
        leading: CircleAvatar(
          backgroundColor: _getStatusColor(status).withOpacity(0.1),
          child: Icon(icon, color: _getStatusColor(status)),
        ),
        title: Text(name, style: const TextStyle(fontWeight: FontWeight.w600)),
        subtitle: Text('$requirement • ${status.toUpperCase()}'),
        trailing: _buildStatusChip(status),
      ),
    );
  }

  Widget _buildStatusChip(String status) {
    Color color;
    IconData icon;

    switch (status) {
      case 'verified':
        color = AppTheme.successColor;
        icon = Icons.check_circle;
        break;
      case 'pending':
        color = AppTheme.warningColor;
        icon = Icons.pending;
        break;
      case 'missing':
        color = AppTheme.errorColor;
        icon = Icons.error;
        break;
      default:
        color = Colors.grey;
        icon = Icons.help;
    }

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      decoration: BoxDecoration(
        color: color.withOpacity(0.1),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: color, width: 1),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, size: 14, color: color),
          const SizedBox(width: 4),
          Text(
            status.toUpperCase(),
            style: TextStyle(color: color, fontSize: 10, fontWeight: FontWeight.w600),
          ),
        ],
      ),
    );
  }

  Widget _buildSignatureCanvas() {
    return SliverToBoxAdapter(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Digital Signature', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),
            Container(
              height: 200,
              decoration: BoxDecoration(
                border: Border.all(color: Colors.grey[300]!),
                borderRadius: BorderRadius.circular(8),
              ),
              child: Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(Icons.draw, size: 60, color: Colors.grey[400]),
                    const SizedBox(height: 16),
                    Text('Signature Canvas', style: TextStyle(fontSize: 18, color: Colors.grey[600])),
                    const SizedBox(height: 8),
                    Text('Draw your signature below', style: TextStyle(fontSize: 14, color: Colors.grey[500])),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildSignatureOptions() {
    return SliverToBoxAdapter(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Signature Options', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),
            Row(
              children: [
                Expanded(
                  child: CustomButton(
                    text: 'Clear',
                    onPressed: _clearSignature,
                    icon: Icons.clear,
                    style: CustomButtonStyle.danger,
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: CustomButton(
                    text: 'Save',
                    onPressed: _saveSignature,
                    icon: Icons.save,
                    style: CustomButtonStyle.success,
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: CustomButton(
                    text: 'Template',
                    onPressed: _useSignatureTemplate,
                    icon: Icons.template,
                    style: CustomButtonStyle.info,
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildFloatingActionButton() {
    return FloatingActionButton.extended(
      onPressed: _showQuickActions,
      icon: const Icon(Icons.add),
      label: const Text('Quick Actions'),
      backgroundColor: AppTheme.primaryColor,
      foregroundColor: Colors.white,
    );
  }

  // Helper methods
  Color _getDocumentTypeColor(String type) {
    switch (type) {
      case 'aadhaar':
        return AppTheme.primaryColor;
      case 'pan':
        return AppTheme.secondaryColor;
      case 'passport':
        return AppTheme.accentColor;
      case 'bank_statement':
        return AppTheme.infoColor;
      default:
        return Colors.grey;
    }
  }

  IconData _getDocumentTypeIcon(String type) {
    switch (type) {
      case 'aadhaar':
        return Icons.credit_card;
      case 'pan':
        return Icons.credit_card;
      case 'passport':
        return Icons.passport;
      case 'bank_statement':
        return Icons.account_balance;
      default:
        return Icons.description;
    }
  }

  Color _getStatusColor(String status) {
    switch (status) {
      case 'verified':
        return AppTheme.successColor;
      case 'pending':
        return AppTheme.warningColor;
      case 'missing':
        return AppTheme.errorColor;
      default:
        return Colors.grey;
    }
  }

  // Event handlers
  void _toggleScanner() {
    setState(() {
      _isScanning = !_isScanning;
    });
  }

  void _toggleFlash() {
    // Implement flash toggle
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Flash toggled'), backgroundColor: AppTheme.infoColor),
    );
  }

  void _scanFromGallery() {
    // Implement gallery scan
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Gallery scan coming soon'), backgroundColor: AppTheme.infoColor),
    );
  }

  void _processScannedData(String data) {
    // Process scanned QR data
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('Processing: $data'), backgroundColor: AppTheme.successColor),
    );
  }

  void _copyScannedData() {
    // Copy to clipboard
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Copied to clipboard'), backgroundColor: AppTheme.successColor),
    );
  }

  void _clearScannedData() {
    setState(() {
      _scannedData = null;
    });
  }

  void _captureFromCamera() {
    // Implement camera capture
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Camera capture coming soon'), backgroundColor: AppTheme.infoColor),
    );
  }

  void _pickFromGallery() {
    // Implement gallery pick
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Gallery pick coming soon'), backgroundColor: AppTheme.infoColor),
    );
  }

  void _pickFromFiles() {
    // Implement file pick
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('File pick coming soon'), backgroundColor: AppTheme.infoColor),
    );
  }

  void _uploadDocument() {
    // Implement document upload
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Document upload coming soon'), backgroundColor: AppTheme.successColor),
    );
  }

  void _handleDocumentAction(String action, Map<String, dynamic> document) {
    switch (action) {
      case 'view':
        _viewDocument(document);
        break;
      case 'download':
        _downloadDocument(document);
        break;
      case 'verify':
        _verifyDocument(document);
        break;
      case 'delete':
        _deleteDocument(document);
        break;
    }
  }

  void _viewDocument(Map<String, dynamic> document) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('Viewing ${document['name']}'), backgroundColor: AppTheme.infoColor),
    );
  }

  void _downloadDocument(Map<String, dynamic> document) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('Downloading ${document['name']}'), backgroundColor: AppTheme.successColor),
    );
  }

  void _verifyDocument(Map<String, dynamic> document) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('Verifying ${document['name']}'), backgroundColor: AppTheme.warningColor),
    );
  }

  void _deleteDocument(Map<String, dynamic> document) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Delete Document'),
        content: Text('Are you sure you want to delete ${document['name']}?'),
        actions: [
          TextButton(onPressed: () => Navigator.pop(context), child: const Text('Cancel')),
          TextButton(
            onPressed: () {
              Navigator.pop(context);
              setState(() {
                _documents.removeWhere((doc) => doc['id'] == document['id']);
              });
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(content: Text('${document['name']} deleted'), backgroundColor: AppTheme.errorColor),
              );
            },
            child: const Text('Delete', style: TextStyle(color: AppTheme.errorColor)),
          ),
        ],
      ),
    );
  }

  void _clearSignature() {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Signature cleared'), backgroundColor: AppTheme.infoColor),
    );
  }

  void _saveSignature() {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Signature saved'), backgroundColor: AppTheme.successColor),
    );
  }

  void _useSignatureTemplate() {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Signature template applied'), backgroundColor: AppTheme.infoColor),
    );
  }

  void _showQuickActions() {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (context) => _buildQuickActionsSheet(),
    );
  }

  Widget _buildQuickActionsSheet() {
    return Container(
      decoration: const BoxDecoration(color: Colors.white, borderRadius: BorderRadius.vertical(top: Radius.circular(20))),
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Text('Quick Actions', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                IconButton(onPressed: () => Navigator.pop(context), icon: const Icon(Icons.close)),
              ],
            ),
            const SizedBox(height: 20),
            _buildQuickActionTile('Scan QR Code', Icons.qr_code_scanner, () { Navigator.pop(context); _toggleScanner(); }),
            _buildQuickActionTile('Upload Document', Icons.upload_file, () { Navigator.pop(context); _showUploadDialog(); }),
            _buildQuickActionTile('Verify KYC', Icons.verified_user, () { Navigator.pop(context); _verifyKYC(); }),
            _buildQuickActionTile('Digital Signature', Icons.draw, () { Navigator.pop(context); _showSignatureDialog(); }),
          ],
        ),
      ),
    );
  }

  Widget _buildQuickActionTile(String title, IconData icon, VoidCallback onTap) {
    return ListTile(
      leading: Icon(icon, color: AppTheme.primaryColor),
      title: Text(title),
      onTap: onTap,
      trailing: const Icon(Icons.arrow_forward_ios, size: 16),
    );
  }

  void _showUploadDialog() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Upload Document'),
        content: const Text('Choose upload method:'),
        actions: [
          TextButton(onPressed: () { Navigator.pop(context); _captureFromCamera(); }, child: const Text('Camera')),
          TextButton(onPressed: () { Navigator.pop(context); _pickFromGallery(); }, child: const Text('Gallery')),
          TextButton(onPressed: () { Navigator.pop(context); _pickFromFiles(); }, child: const Text('Files')),
        ],
      ),
    );
  }

  void _verifyKYC() {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('KYC verification started'), backgroundColor: AppTheme.infoColor),
    );
  }

  void _showSignatureDialog() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Digital Signature'),
        content: const Text('Choose signature method:'),
        actions: [
          TextButton(onPressed: () { Navigator.pop(context); _clearSignature(); }, child: const Text('Draw')),
          TextButton(onPressed: () { Navigator.pop(context); _useSignatureTemplate(); }, child: const Text('Template')),
          TextButton(onPressed: () { Navigator.pop(context); _saveSignature(); }, child: const Text('Save')),
        ],
      ),
    );
  }

  void _showScanHistory() {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Scan history coming soon'), backgroundColor: AppTheme.infoColor),
    );
  }

  void _showScannerSettings() {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Scanner settings coming soon'), backgroundColor: AppTheme.infoColor),
    );
  }
}

