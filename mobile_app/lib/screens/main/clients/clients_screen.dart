import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../../../config/app_theme.dart';
import '../../../widgets/common/loading_overlay.dart';

class ClientsScreen extends StatefulWidget {
  const ClientsScreen({Key? key}) : super(key: key);

  @override
  State<ClientsScreen> createState() => _ClientsScreenState();
}

class _ClientsScreenState extends State<ClientsScreen> {
  bool _isLoading = false;
  List<Map<String, dynamic>> _clients = [];

  @override
  void initState() {
    super.initState();
    _loadClients();
  }

  Future<void> _loadClients() async {
    setState(() {
      _isLoading = true;
    });

    try {
      // Simulate API call
      await Future.delayed(const Duration(seconds: 1));
      
      setState(() {
        _clients = [
          {
            'id': 'C001',
            'name': 'Rahul Kumar',
            'phone': '+91 98765 43210',
            'village': 'Village Center #VC001',
            'status': 'Active',
            'totalLoans': 3,
            'totalAmount': 150000,
          },
          {
            'id': 'C002',
            'name': 'Priya Sharma',
            'phone': '+91 87654 32109',
            'village': 'Village Center #VC002',
            'status': 'Active',
            'totalLoans': 2,
            'totalAmount': 100000,
          },
          {
            'id': 'C003',
            'name': 'Amit Patel',
            'phone': '+91 76543 21098',
            'village': 'Village Center #VC003',
            'status': 'Inactive',
            'totalLoans': 1,
            'totalAmount': 50000,
          },
        ];
      });
    } catch (e) {
      Get.snackbar(
        'Error',
        'Failed to load clients: $e',
        snackPosition: SnackPosition.BOTTOM,
        backgroundColor: AppTheme.errorColor,
        colorText: Colors.white,
      );
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Clients'),
        backgroundColor: AppTheme.primaryColor,
        foregroundColor: Colors.white,
        elevation: 0,
        actions: [
          IconButton(
            onPressed: () => _showSearchDialog(),
            icon: const Icon(Icons.search),
          ),
          IconButton(
            onPressed: () => _showFilterDialog(),
            icon: const Icon(Icons.filter_list),
          ),
        ],
      ),
      body: LoadingOverlay(
        isLoading: _isLoading,
        child: RefreshIndicator(
          onRefresh: _loadClients,
          child: _clients.isEmpty && !_isLoading
              ? _buildEmptyState()
              : ListView.builder(
                  padding: const EdgeInsets.all(16),
                  itemCount: _clients.length,
                  itemBuilder: (context, index) {
                    final client = _clients[index];
                    return _buildClientCard(client);
                  },
                ),
        ),
      ),
    );
  }

  Widget _buildEmptyState() {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(
            Icons.people_outline,
            size: 80,
            color: AppTheme.textSecondaryColor.withOpacity(0.5),
          ),
          const SizedBox(height: 16),
          Text(
            'No Clients Found',
            style: AppTheme.lightTheme.textTheme.headlineSmall?.copyWith(
              color: AppTheme.textSecondaryColor,
            ),
          ),
          const SizedBox(height: 8),
          Text(
            'Start by adding your first client',
            style: AppTheme.lightTheme.textTheme.bodyMedium?.copyWith(
              color: AppTheme.textSecondaryColor.withOpacity(0.7),
            ),
          ),
          const SizedBox(height: 24),
          ElevatedButton.icon(
            onPressed: () => _addNewClient(),
            icon: const Icon(Icons.add),
            label: const Text('Add Client'),
            style: ElevatedButton.styleFrom(
              backgroundColor: AppTheme.primaryColor,
              foregroundColor: Colors.white,
              padding: const EdgeInsets.symmetric(
                horizontal: 24,
                vertical: 12,
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildClientCard(Map<String, dynamic> client) {
    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.05),
            blurRadius: 10,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: ListTile(
        contentPadding: const EdgeInsets.all(16),
        leading: CircleAvatar(
          backgroundColor: AppTheme.primaryColor.withOpacity(0.1),
          child: Text(
            client['name'].substring(0, 1),
            style: TextStyle(
              color: AppTheme.primaryColor,
              fontWeight: FontWeight.bold,
            ),
          ),
        ),
        title: Text(
          client['name'],
          style: AppTheme.lightTheme.textTheme.titleMedium?.copyWith(
            fontWeight: FontWeight.w600,
          ),
        ),
        subtitle: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const SizedBox(height: 4),
            Text(
              client['phone'],
              style: AppTheme.lightTheme.textTheme.bodyMedium?.copyWith(
                color: AppTheme.textSecondaryColor,
              ),
            ),
            const SizedBox(height: 2),
            Text(
              client['village'],
              style: AppTheme.lightTheme.textTheme.bodySmall?.copyWith(
                color: AppTheme.textSecondaryColor.withOpacity(0.7),
              ),
            ),
            const SizedBox(height: 8),
            Row(
              children: [
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 8,
                    vertical: 4,
                  ),
                  decoration: BoxDecoration(
                    color: client['status'] == 'Active'
                        ? AppTheme.successColor.withOpacity(0.1)
                        : AppTheme.errorColor.withOpacity(0.1),
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(
                      color: client['status'] == 'Active'
                          ? AppTheme.successColor.withOpacity(0.3)
                          : AppTheme.errorColor.withOpacity(0.3),
                    ),
                  ),
                  child: Text(
                    client['status'],
                    style: AppTheme.lightTheme.textTheme.labelSmall?.copyWith(
                      color: client['status'] == 'Active'
                          ? AppTheme.successColor
                          : AppTheme.errorColor,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ),
                const Spacer(),
                Text(
                  '${client['totalLoans']} loans',
                  style: AppTheme.lightTheme.textTheme.bodySmall?.copyWith(
                    color: AppTheme.textSecondaryColor,
                  ),
                ),
              ],
            ),
          ],
        ),
        trailing: IconButton(
          onPressed: () => _showClientOptions(client),
          icon: const Icon(Icons.more_vert),
        ),
        onTap: () => _viewClientDetails(client),
      ),
    );
  }

  void _addNewClient() {
    Get.snackbar(
      'Add Client',
      'Add client functionality coming soon',
      snackPosition: SnackPosition.BOTTOM,
    );
  }

  void _viewClientDetails(Map<String, dynamic> client) {
    Get.snackbar(
      'View Client',
      'Viewing details for ${client['name']}',
      snackPosition: SnackPosition.BOTTOM,
    );
  }

  void _showClientOptions(Map<String, dynamic> client) {
    showModalBottomSheet(
      context: context,
      backgroundColor: Colors.transparent,
      builder: (context) => Container(
        decoration: const BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
        ),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Container(
              margin: const EdgeInsets.only(top: 12),
              width: 40,
              height: 4,
              decoration: BoxDecoration(
                color: AppTheme.textSecondaryColor.withOpacity(0.3),
                borderRadius: BorderRadius.circular(2),
              ),
            ),
            const SizedBox(height: 20),
            ListTile(
              leading: const Icon(Icons.visibility),
              title: const Text('View Details'),
              onTap: () {
                Navigator.pop(context);
                _viewClientDetails(client);
              },
            ),
            ListTile(
              leading: const Icon(Icons.edit),
              title: const Text('Edit Client'),
              onTap: () {
                Navigator.pop(context);
                _editClient(client);
              },
            ),
            ListTile(
              leading: const Icon(Icons.add_business),
              title: const Text('New Loan'),
              onTap: () {
                Navigator.pop(context);
                _createNewLoan(client);
              },
            ),
            ListTile(
              leading: const Icon(Icons.location_on),
              title: const Text('Field Visit'),
              onTap: () {
                Navigator.pop(context);
                _scheduleFieldVisit(client);
              },
            ),
            ListTile(
              leading: const Icon(Icons.qr_code),
              title: const Text('Generate QR'),
              onTap: () {
                Navigator.pop(context);
                _generateQRCode(client);
              },
            ),
            const SizedBox(height: 20),
          ],
        ),
      ),
    );
  }

  void _editClient(Map<String, dynamic> client) {
    Get.snackbar(
      'Edit Client',
      'Editing ${client['name']}',
      snackPosition: SnackPosition.BOTTOM,
    );
  }

  void _createNewLoan(Map<String, dynamic> client) {
    Get.snackbar(
      'New Loan',
      'Creating loan for ${client['name']}',
      snackPosition: SnackPosition.BOTTOM,
    );
  }

  void _scheduleFieldVisit(Map<String, dynamic> client) {
    Get.snackbar(
      'Field Visit',
      'Scheduling visit for ${client['name']}',
      snackPosition: SnackPosition.BOTTOM,
    );
  }

  void _generateQRCode(Map<String, dynamic> client) {
    Get.snackbar(
      'QR Code',
      'Generating QR for ${client['name']}',
      snackPosition: SnackPosition.BOTTOM,
    );
  }

  void _showSearchDialog() {
    Get.snackbar(
      'Search',
      'Search functionality coming soon',
      snackPosition: SnackPosition.BOTTOM,
    );
  }

  void _showFilterDialog() {
    Get.snackbar(
      'Filter',
      'Filter functionality coming soon',
      snackPosition: SnackPosition.BOTTOM,
    );
  }
}

