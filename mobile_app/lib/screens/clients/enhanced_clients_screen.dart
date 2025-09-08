import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:get/get.dart';
import 'package:intl/intl.dart';

import '../../config/app_theme.dart';
import '../../models/sml_models.dart';
import '../../providers/sml_providers.dart';
import '../../widgets/common/custom_button.dart';
import '../../widgets/common/custom_text_field.dart';
import '../../widgets/common/loading_overlay.dart';
import '../../utils/constants.dart';

class EnhancedClientsScreen extends StatefulWidget {
  const EnhancedClientsScreen({Key? key}) : super(key: key);

  @override
  State<EnhancedClientsScreen> createState() => _EnhancedClientsScreenState();
}

class _EnhancedClientsScreenState extends State<EnhancedClientsScreen>
    with TickerProviderStateMixin {
  late AnimationController _animationController;
  late Animation<double> _fadeAnimation;
  late Animation<Offset> _slideAnimation;

  final TextEditingController _searchController = TextEditingController();
  final ScrollController _scrollController = ScrollController();
  
  String _selectedFilter = 'all';
  String _selectedSortBy = 'name';
  String _selectedSortOrder = 'asc';

  @override
  void initState() {
    super.initState();
    _initializeAnimations();
    _loadInitialData();
    _setupScrollListener();
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

  void _loadInitialData() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      context.read<SMLClientProvider>().loadClients(refresh: true);
    });
  }

  void _setupScrollListener() {
    _scrollController.addListener(() {
      if (_scrollController.position.pixels >=
          _scrollController.position.maxScrollExtent - 200) {
        _loadMoreData();
      }
    });
  }

  void _loadMoreData() {
    final provider = context.read<SMLClientProvider>();
    if (provider.hasMoreData && !provider.isLoading) {
      provider.loadClients();
    }
  }

  @override
  void dispose() {
    _animationController.dispose();
    _searchController.dispose();
    _scrollController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppTheme.backgroundColor,
      body: FadeTransition(
        opacity: _fadeAnimation,
        child: SlideTransition(
          position: _slideAnimation,
          child: CustomScrollView(
            controller: _scrollController,
            slivers: [
              _buildSliverAppBar(),
              _buildSearchAndFilters(),
              _buildClientsList(),
            ],
          ),
        ),
      ),
      floatingActionButton: _buildFloatingActionButton(),
    );
  }

  Widget _buildSliverAppBar() {
    return SliverAppBar(
      expandedHeight: 120,
      floating: false,
      pinned: true,
      backgroundColor: AppTheme.primaryColor,
      elevation: 0,
      flexibleSpace: FlexibleSpaceBar(
        title: Text(
          'Client Management',
          style: AppTheme.appBarTitleStyle.copyWith(
            color: Colors.white,
            fontWeight: FontWeight.w600,
          ),
        ),
        background: Container(
          decoration: BoxDecoration(
            gradient: AppTheme.primaryGradient,
          ),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.end,
            children: [
              Padding(
                padding: const EdgeInsets.only(bottom: 16.0),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [
                    _buildQuickStat('Total Clients', '1,247', Icons.people),
                    _buildQuickStat('Active Clients', '1,189', Icons.check_circle),
                    _buildQuickStat('New This Month', '58', Icons.trending_up),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
      actions: [
        IconButton(
          icon: const Icon(Icons.filter_list, color: Colors.white),
          onPressed: _showAdvancedFilters,
        ),
        IconButton(
          icon: const Icon(Icons.more_vert, color: Colors.white),
          onPressed: _showMoreOptions,
        ),
      ],
    );
  }

  Widget _buildQuickStat(String label, String value, IconData icon) {
    return Column(
      children: [
        Icon(icon, color: Colors.white70, size: 20),
        const SizedBox(height: 4),
        Text(
          value,
          style: const TextStyle(
            color: Colors.white,
            fontSize: 18,
            fontWeight: FontWeight.bold,
          ),
        ),
        Text(
          label,
          style: const TextStyle(
            color: Colors.white70,
            fontSize: 12,
          ),
        ),
      ],
    );
  }

  Widget _buildSearchAndFilters() {
    return SliverToBoxAdapter(
      child: Container(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            // Search Bar
            CustomTextField(
              controller: _searchController,
              hintText: 'Search clients by name, code, or phone...',
              prefixIcon: Icons.search,
              onChanged: _onSearchChanged,
              suffixIcon: _searchController.text.isNotEmpty
                  ? Icons.clear
                  : null,
              onSuffixIconPressed: _clearSearch,
            ),
            const SizedBox(height: 16),
            // Quick Filters
            SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              child: Row(
                children: [
                  _buildFilterChip('All', 'all'),
                  _buildFilterChip('Active', 'active'),
                  _buildFilterChip('Inactive', 'inactive'),
                  _buildFilterChip('New', 'new'),
                  _buildFilterChip('VIP', 'vip'),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildFilterChip(String label, String value) {
    final isSelected = _selectedFilter == value;
    return Padding(
      padding: const EdgeInsets.only(right: 8.0),
      child: FilterChip(
        label: Text(label),
        selected: isSelected,
        onSelected: (selected) => _onFilterChanged(value),
        selectedColor: AppTheme.primaryColor.withOpacity(0.2),
        checkmarkColor: AppTheme.primaryColor,
        labelStyle: TextStyle(
          color: isSelected ? AppTheme.primaryColor : AppTheme.textColor,
          fontWeight: isSelected ? FontWeight.w600 : FontWeight.normal,
        ),
      ),
    );
  }

  Widget _buildClientsList() {
    return Consumer<SMLClientProvider>(
      builder: (context, clientProvider, child) {
        if (clientProvider.isLoading && clientProvider.clients.isEmpty) {
          return const SliverFillRemaining(
            child: Center(
              child: CircularProgressIndicator(),
            ),
          );
        }

        if (clientProvider.clients.isEmpty) {
          return SliverFillRemaining(
            child: _buildEmptyState(),
          );
        }

        return SliverList(
          delegate: SliverChildBuilderDelegate(
            (context, index) {
              if (index >= clientProvider.clients.length) {
                if (clientProvider.hasMoreData) {
                  return _buildLoadingMore();
                }
                return const SizedBox.shrink();
              }

              final client = clientProvider.clients[index];
              return _buildClientCard(client, index);
            },
            childCount: clientProvider.clients.length + (clientProvider.hasMoreData ? 1 : 0),
          ),
        );
      },
    );
  }

  Widget _buildClientCard(SMLClient client, int index) {
    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: Card(
        elevation: 2,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12),
        ),
        child: InkWell(
          onTap: () => _onClientTap(client),
          borderRadius: BorderRadius.circular(12),
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    CircleAvatar(
                      radius: 25,
                      backgroundColor: AppTheme.primaryColor.withOpacity(0.1),
                      child: Text(
                        client.initials,
                        style: TextStyle(
                          color: AppTheme.primaryColor,
                          fontWeight: FontWeight.bold,
                          fontSize: 18,
                        ),
                      ),
                    ),
                    const SizedBox(width: 16),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            client.fullName,
                            style: const TextStyle(
                              fontSize: 18,
                              fontWeight: FontWeight.w600,
                            ),
                          ),
                          const SizedBox(height: 4),
                          Text(
                            'Code: ${client.clientCode}',
                            style: TextStyle(
                              color: AppTheme.textColor.withOpacity(0.7),
                              fontSize: 14,
                            ),
                          ),
                          if (client.phoneNumber != null) ...[
                            const SizedBox(height: 2),
                            Text(
                              client.phoneNumber!,
                              style: TextStyle(
                                color: AppTheme.textColor.withOpacity(0.7),
                                fontSize: 14,
                              ),
                            ),
                          ],
                        ],
                      ),
                    ),
                    _buildStatusChip(client.status),
                  ],
                ),
                const SizedBox(height: 16),
                Row(
                  children: [
                    _buildInfoItem('Age', '${client.age} years'),
                    _buildInfoItem('Village', client.village ?? 'N/A'),
                    _buildInfoItem('Occupation', client.occupation ?? 'N/A'),
                  ],
                ),
                const SizedBox(height: 16),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [
                    _buildActionButton(
                      'View Details',
                      Icons.visibility,
                      () => _onClientTap(client),
                    ),
                    _buildActionButton(
                      'Edit',
                      Icons.edit,
                      () => _onEditClient(client),
                    ),
                    _buildActionButton(
                      'New Loan',
                      Icons.add_circle,
                      () => _onNewLoan(client),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildStatusChip(String status) {
    Color color;
    String label;
    
    switch (status.toLowerCase()) {
      case 'active':
        color = AppTheme.successColor;
        label = 'Active';
        break;
      case 'inactive':
        color = AppTheme.errorColor;
        label = 'Inactive';
        break;
      case 'new':
        color = AppTheme.infoColor;
        label = 'New';
        break;
      case 'vip':
        color = AppTheme.warningColor;
        label = 'VIP';
        break;
      default:
        color = AppTheme.textColor.withOpacity(0.5);
        label = status;
    }

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      decoration: BoxDecoration(
        color: color.withOpacity(0.1),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: color.withOpacity(0.3)),
      ),
      child: Text(
        label,
        style: TextStyle(
          color: color,
          fontSize: 12,
          fontWeight: FontWeight.w600,
        ),
      ),
    );
  }

  Widget _buildInfoItem(String label, String value) {
    return Expanded(
      child: Column(
        children: [
          Text(
            label,
            style: TextStyle(
              color: AppTheme.textColor.withOpacity(0.6),
              fontSize: 12,
            ),
          ),
          const SizedBox(height: 2),
          Text(
            value,
            style: const TextStyle(
              fontSize: 14,
              fontWeight: FontWeight.w500,
            ),
            textAlign: TextAlign.center,
            maxLines: 1,
            overflow: TextOverflow.ellipsis,
          ),
        ],
      ),
    );
  }

  Widget _buildActionButton(String label, IconData icon, VoidCallback onPressed) {
    return Expanded(
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 4),
        child: OutlinedButton.icon(
          onPressed: onPressed,
          icon: Icon(icon, size: 16),
          label: Text(
            label,
            style: const TextStyle(fontSize: 12),
          ),
          style: OutlinedButton.styleFrom(
            padding: const EdgeInsets.symmetric(vertical: 8),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(8),
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildEmptyState() {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Icon(
          Icons.people_outline,
          size: 80,
          color: AppTheme.textColor.withOpacity(0.3),
        ),
        const SizedBox(height: 16),
        Text(
          'No Clients Found',
          style: TextStyle(
            fontSize: 24,
            fontWeight: FontWeight.w600,
            color: AppTheme.textColor.withOpacity(0.7),
          ),
        ),
        const SizedBox(height: 8),
        Text(
          'Start by adding your first client',
          style: TextStyle(
            fontSize: 16,
            color: AppTheme.textColor.withOpacity(0.5),
          ),
        ),
        const SizedBox(height: 24),
        CustomButton(
          text: 'Add New Client',
          onPressed: _onAddNewClient,
          icon: Icons.add,
        ),
      ],
    );
  }

  Widget _buildLoadingMore() {
    return const Padding(
      padding: EdgeInsets.all(16),
      child: Center(
        child: CircularProgressIndicator(),
      ),
    );
  }

  Widget _buildFloatingActionButton() {
    return FloatingActionButton.extended(
      onPressed: _onAddNewClient,
      backgroundColor: AppTheme.primaryColor,
      icon: const Icon(Icons.add, color: Colors.white),
      label: const Text(
        'Add Client',
        style: TextStyle(color: Colors.white),
      ),
    );
  }

  // Event Handlers
  void _onSearchChanged(String query) {
    context.read<SMLClientProvider>().searchClients(query);
  }

  void _clearSearch() {
    _searchController.clear();
    context.read<SMLClientProvider>().searchClients('');
  }

  void _onFilterChanged(String filter) {
    setState(() {
      _selectedFilter = filter;
    });
    context.read<SMLClientProvider>().filterClientsByStatus(filter);
  }

  void _onClientTap(SMLClient client) {
    // Navigate to client details screen
    Get.toNamed('/client-details', arguments: client);
  }

  void _onEditClient(SMLClient client) {
    // Navigate to edit client screen
    Get.toNamed('/edit-client', arguments: client);
  }

  void _onNewLoan(SMLClient client) {
    // Navigate to new loan screen
    Get.toNamed('/new-loan', arguments: client);
  }

  void _onAddNewClient() {
    // Navigate to add client screen
    Get.toNamed('/add-client');
  }

  void _showAdvancedFilters() {
    // Show advanced filter dialog
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (context) => _buildAdvancedFiltersSheet(),
    );
  }

  void _showMoreOptions() {
    // Show more options menu
    showModalBottomSheet(
      context: context,
      backgroundColor: Colors.transparent,
      builder: (context) => _buildMoreOptionsSheet(),
    );
  }

  Widget _buildAdvancedFiltersSheet() {
    return Container(
      height: MediaQuery.of(context).size.height * 0.6,
      decoration: const BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      child: Column(
        children: [
          Container(
            width: 40,
            height: 4,
            margin: const EdgeInsets.symmetric(vertical: 12),
            decoration: BoxDecoration(
              color: Colors.grey[300],
              borderRadius: BorderRadius.circular(2),
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(16),
            child: Text(
              'Advanced Filters',
              style: AppTheme.headingStyle,
            ),
          ),
          Expanded(
            child: ListView(
              padding: const EdgeInsets.all(16),
              children: [
                _buildFilterSection('Sort By', [
                  'Name',
                  'Code',
                  'Created Date',
                  'Last Updated',
                ], _selectedSortBy, (value) {
                  setState(() {
                    _selectedSortBy = value;
                  });
                }),
                const SizedBox(height: 24),
                _buildFilterSection('Sort Order', [
                  'Ascending',
                  'Descending',
                ], _selectedSortOrder, (value) {
                  setState(() {
                    _selectedSortOrder = value;
                  });
                }),
              ],
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(16),
            child: Row(
              children: [
                Expanded(
                  child: OutlinedButton(
                    onPressed: () => Get.back(),
                    child: const Text('Reset'),
                  ),
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: CustomButton(
                    text: 'Apply Filters',
                    onPressed: () {
                      _applyAdvancedFilters();
                      Get.back();
                    },
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildFilterSection(String title, List<String> options, String selected, Function(String) onChanged) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          title,
          style: const TextStyle(
            fontSize: 16,
            fontWeight: FontWeight.w600,
          ),
        ),
        const SizedBox(height: 12),
        Wrap(
          spacing: 8,
          children: options.map((option) {
            final isSelected = selected == option.toLowerCase();
            return ChoiceChip(
              label: Text(option),
              selected: isSelected,
              onSelected: (selected) => onChanged(option.toLowerCase()),
              selectedColor: AppTheme.primaryColor.withOpacity(0.2),
              labelStyle: TextStyle(
                color: isSelected ? AppTheme.primaryColor : AppTheme.textColor,
                fontWeight: isSelected ? FontWeight.w600 : FontWeight.normal,
              ),
            );
          }).toList(),
        ),
      ],
    );
  }

  Widget _buildMoreOptionsSheet() {
    return Container(
      decoration: const BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Container(
            width: 40,
            height: 4,
            margin: const EdgeInsets.symmetric(vertical: 12),
            decoration: BoxDecoration(
              color: Colors.grey[300],
              borderRadius: BorderRadius.circular(2),
            ),
          ),
          ListTile(
            leading: const Icon(Icons.file_download),
            title: const Text('Export Clients'),
            onTap: () {
              Get.back();
              _exportClients();
            },
          ),
          ListTile(
            leading: const Icon(Icons.settings),
            title: const Text('Client Settings'),
            onTap: () {
              Get.back();
              _openClientSettings();
            },
          ),
          ListTile(
            leading: const Icon(Icons.help),
            title: const Text('Help & Support'),
            onTap: () {
              Get.back();
              _openHelpSupport();
            },
          ),
          const SizedBox(height: 16),
        ],
      ),
    );
  }

  void _applyAdvancedFilters() {
    // Apply the selected filters
    final provider = context.read<SMLClientProvider>();
    provider.loadClients(refresh: true);
  }

  void _exportClients() {
    // Implement client export functionality
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Export functionality coming soon!')),
    );
  }

  void _openClientSettings() {
    // Navigate to client settings
    Get.toNamed('/client-settings');
  }

  void _openHelpSupport() {
    // Navigate to help and support
    Get.toNamed('/help-support');
  }
}

