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

class EnhancedLoansScreen extends StatefulWidget {
  const EnhancedLoansScreen({Key? key}) : super(key: key);

  @override
  State<EnhancedLoansScreen> createState() => _EnhancedLoansScreenState();
}

class _EnhancedLoansScreenState extends State<EnhancedLoansScreen>
    with TickerProviderStateMixin {
  late AnimationController _animationController;
  late Animation<double> _fadeAnimation;
  late Animation<Offset> _slideAnimation;

  final TextEditingController _searchController = TextEditingController();
  final ScrollController _scrollController = ScrollController();

  String _selectedFilter = 'all';
  String _selectedSortBy = 'application_date';
  String _selectedSortOrder = 'desc';
  String _selectedLoanType = 'all';

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
      context.read<SMLLoanProvider>().loadLoans();
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
    final provider = context.read<SMLLoanProvider>();
    if (provider.hasMoreData && !provider.isLoading) {
      provider.loadMoreLoans();
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
      body: LoadingOverlay(
        isLoading: context.watch<SMLLoanProvider>().isLoading,
        child: CustomScrollView(
          controller: _scrollController,
          slivers: [
            _buildSliverAppBar(),
            _buildSearchAndFilters(),
            _buildLoansList(),
          ],
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
      flexibleSpace: FlexibleSpaceBar(
        title: const Text(
          'Loan Management',
          style: TextStyle(
            color: Colors.white,
            fontWeight: FontWeight.bold,
          ),
        ),
        background: Container(
          decoration: BoxDecoration(
            gradient: AppTheme.primaryGradient,
          ),
          child: Padding(
            padding: const EdgeInsets.fromLTRB(16, 60, 16, 16),
            child: Row(
              children: [
                Expanded(
                  child: _buildQuickStat('Total Loans', '0', Icons.account_balance),
                ),
                Expanded(
                  child: _buildQuickStat('Active', '0', Icons.check_circle),
                ),
                Expanded(
                  child: _buildQuickStat('Pending', '0', Icons.pending),
                ),
                Expanded(
                  child: _buildQuickStat('Overdue', '0', Icons.warning),
                ),
              ],
            ),
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
      mainAxisAlignment: MainAxisAlignment.center,
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
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            _buildSearchBar(),
            const SizedBox(height: 16),
            _buildQuickFilters(),
          ],
        ),
      ),
    );
  }

  Widget _buildSearchBar() {
    return CustomTextField(
      controller: _searchController,
      hintText: 'Search loans by client name, loan code...',
      prefixIcon: Icons.search,
      onChanged: _onSearchChanged,
      suffixIcon: _searchController.text.isNotEmpty
          ? Icons.clear
          : null,
      onSuffixIconPressed: _clearSearch,
    );
  }

  Widget _buildQuickFilters() {
    return SingleChildScrollView(
      scrollDirection: Axis.horizontal,
      child: Row(
        children: [
          _buildFilterChip('All', 'all'),
          const SizedBox(width: 8),
          _buildFilterChip('Active', 'active'),
          const SizedBox(width: 8),
          _buildFilterChip('Pending', 'pending'),
          const SizedBox(width: 8),
          _buildFilterChip('Approved', 'approved'),
          const SizedBox(width: 8),
          _buildFilterChip('Disbursed', 'disbursed'),
          const SizedBox(width: 8),
          _buildFilterChip('Overdue', 'overdue'),
        ],
      ),
    );
  }

  Widget _buildFilterChip(String label, String value) {
    final isSelected = _selectedFilter == value;
    return FilterChip(
      label: Text(label),
      selected: isSelected,
      onSelected: (selected) => _onFilterChanged(value),
      selectedColor: AppTheme.primaryColor.withOpacity(0.2),
      checkmarkColor: AppTheme.primaryColor,
      backgroundColor: Colors.grey[200],
      labelStyle: TextStyle(
        color: isSelected ? AppTheme.primaryColor : Colors.black87,
        fontWeight: isSelected ? FontWeight.w600 : FontWeight.normal,
      ),
    );
  }

  Widget _buildLoansList() {
    return Consumer<SMLLoanProvider>(
      builder: (context, provider, child) {
        if (provider.loans.isEmpty && !provider.isLoading) {
          return _buildEmptyState();
        }

        return SliverList(
          delegate: SliverChildBuilderDelegate(
            (context, index) {
              if (index >= provider.loans.length) {
                if (provider.hasMoreData) {
                  return _buildLoadingMore();
                }
                return const SizedBox.shrink();
              }

              final loan = provider.loans[index];
              return _buildLoanCard(loan);
            },
            childCount: provider.loans.length + (provider.hasMoreData ? 1 : 0),
          ),
        );
      },
    );
  }

  Widget _buildLoanCard(SMLLoanApplication loan) {
    return FadeTransition(
      opacity: _fadeAnimation,
      child: SlideTransition(
        position: _slideAnimation,
        child: Card(
          margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
          elevation: 4,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(12),
          ),
          child: InkWell(
            onTap: () => _onLoanTap(loan),
            borderRadius: BorderRadius.circular(12),
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              loan.loanCode,
                              style: const TextStyle(
                                fontSize: 16,
                                fontWeight: FontWeight.bold,
                                color: Colors.black87,
                              ),
                            ),
                            const SizedBox(height: 4),
                            Text(
                              'Client: ${loan.clientName ?? 'N/A'}',
                              style: TextStyle(
                                fontSize: 14,
                                color: Colors.grey[600],
                              ),
                            ),
                          ],
                        ),
                      ),
                      _buildStatusChip(loan.status),
                    ],
                  ),
                  const SizedBox(height: 16),
                  Row(
                    children: [
                      Expanded(
                        child: _buildLoanInfo(
                          'Amount',
                          loan.formattedLoanAmount,
                          Icons.currency_rupee,
                        ),
                      ),
                      Expanded(
                        child: _buildLoanInfo(
                          'EMI',
                          loan.formattedEMIAmount,
                          Icons.payment,
                        ),
                      ),
                      Expanded(
                        child: _buildLoanInfo(
                          'Tenure',
                          '${loan.tenure} months',
                          Icons.calendar_today,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),
                  Row(
                    children: [
                      Expanded(
                        child: _buildLoanInfo(
                          'Interest',
                          '${loan.interestRate}%',
                          Icons.percent,
                        ),
                      ),
                      Expanded(
                        child: _buildLoanInfo(
                          'Purpose',
                          loan.purpose ?? 'N/A',
                          Icons.category,
                        ),
                      ),
                      Expanded(
                        child: _buildLoanInfo(
                          'Applied',
                          loan.formattedApplicationDate,
                          Icons.date_range,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                    children: [
                      _buildActionButton(
                        'View Details',
                        Icons.visibility,
                        () => _onViewDetails(loan),
                        AppTheme.primaryColor,
                      ),
                      _buildActionButton(
                        'Edit',
                        Icons.edit,
                        () => _onEditLoan(loan),
                        AppTheme.secondaryColor,
                      ),
                      _buildActionButton(
                        'Documents',
                        Icons.description,
                        () => _onViewDocuments(loan),
                        AppTheme.accentColor,
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildStatusChip(String status) {
    Color color;
    IconData icon;

    switch (status.toLowerCase()) {
      case 'active':
        color = AppTheme.successColor;
        icon = Icons.check_circle;
        break;
      case 'pending':
        color = AppTheme.warningColor;
        icon = Icons.pending;
        break;
      case 'approved':
        color = AppTheme.infoColor;
        icon = Icons.approval;
        break;
      case 'disbursed':
        color = AppTheme.primaryColor;
        icon = Icons.account_balance_wallet;
        break;
      case 'overdue':
        color = AppTheme.errorColor;
        icon = Icons.warning;
        break;
      default:
        color = Colors.grey;
        icon = Icons.help;
    }

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      decoration: BoxDecoration(
        color: color.withOpacity(0.1),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: color, width: 1),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, size: 16, color: color),
          const SizedBox(width: 4),
          Text(
            status.toUpperCase(),
            style: TextStyle(
              color: color,
              fontSize: 12,
              fontWeight: FontWeight.w600,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildLoanInfo(String label, String value, IconData icon) {
    return Column(
      children: [
        Icon(icon, size: 20, color: AppTheme.primaryColor),
        const SizedBox(height: 4),
        Text(
          value,
          style: const TextStyle(
            fontSize: 14,
            fontWeight: FontWeight.w600,
            color: Colors.black87,
          ),
          textAlign: TextAlign.center,
          maxLines: 2,
          overflow: TextOverflow.ellipsis,
        ),
        Text(
          label,
          style: TextStyle(
            fontSize: 12,
            color: Colors.grey[600],
          ),
          textAlign: TextAlign.center,
        ),
      ],
    );
  }

  Widget _buildActionButton(
    String text,
    IconData icon,
    VoidCallback onPressed,
    Color color,
  ) {
    return Expanded(
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 4),
        child: ElevatedButton.icon(
          onPressed: onPressed,
          icon: Icon(icon, size: 16),
          label: Text(
            text,
            style: const TextStyle(fontSize: 12),
          ),
          style: ElevatedButton.styleFrom(
            backgroundColor: color,
            foregroundColor: Colors.white,
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
    return SliverFillRemaining(
      child: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              Icons.account_balance_outlined,
              size: 80,
              color: Colors.grey[400],
            ),
            const SizedBox(height: 16),
            Text(
              'No Loans Found',
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
                color: Colors.grey[600],
              ),
            ),
            const SizedBox(height: 8),
            Text(
              'Start by creating your first loan application',
              style: TextStyle(
                fontSize: 16,
                color: Colors.grey[500],
              ),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 24),
            CustomButton(
              text: 'Add New Loan',
              onPressed: _onAddNewLoan,
              icon: Icons.add,
              style: CustomButtonStyle.primary,
            ),
          ],
        ),
      ),
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
      onPressed: _onAddNewLoan,
      icon: const Icon(Icons.add),
      label: const Text('Add Loan'),
      backgroundColor: AppTheme.primaryColor,
      foregroundColor: Colors.white,
    );
  }

  void _onSearchChanged(String query) {
    context.read<SMLLoanProvider>().searchLoans(query);
  }

  void _clearSearch() {
    _searchController.clear();
    context.read<SMLLoanProvider>().clearSearch();
  }

  void _onFilterChanged(String filter) {
    setState(() {
      _selectedFilter = filter;
    });
    context.read<SMLLoanProvider>().filterLoansByStatus(filter);
  }

  void _onLoanTap(SMLLoanApplication loan) {
    // Navigate to loan details screen
    Get.toNamed('/loan-details', arguments: loan);
  }

  void _onViewDetails(SMLLoanApplication loan) {
    // Navigate to loan details screen
    Get.toNamed('/loan-details', arguments: loan);
  }

  void _onEditLoan(SMLLoanApplication loan) {
    // Navigate to edit loan screen
    Get.toNamed('/edit-loan', arguments: loan);
  }

  void _onViewDocuments(SMLLoanApplication loan) {
    // Navigate to documents screen
    Get.toNamed('/loan-documents', arguments: loan);
  }

  void _onAddNewLoan() {
    // Navigate to add loan screen
    Get.toNamed('/add-loan');
  }

  void _showAdvancedFilters() {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (context) => _buildAdvancedFiltersSheet(),
    );
  }

  Widget _buildAdvancedFiltersSheet() {
    return Container(
      decoration: const BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Text(
                  'Advanced Filters',
                  style: TextStyle(
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                IconButton(
                  onPressed: () => Navigator.pop(context),
                  icon: const Icon(Icons.close),
                ),
              ],
            ),
            const SizedBox(height: 20),
            const Text(
              'Sort By',
              style: TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.w600,
              ),
            ),
            const SizedBox(height: 12),
            Wrap(
              spacing: 8,
              children: [
                _buildChoiceChip('Application Date', 'application_date'),
                _buildChoiceChip('Loan Amount', 'loan_amount'),
                _buildChoiceChip('Client Name', 'client_name'),
                _buildChoiceChip('Status', 'status'),
                _buildChoiceChip('Created Date', 'created_date'),
              ],
            ),
            const SizedBox(height: 20),
            const Text(
              'Sort Order',
              style: TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.w600,
              ),
            ),
            const SizedBox(height: 12),
            Wrap(
              spacing: 8,
              children: [
                _buildChoiceChip('Ascending', 'asc'),
                _buildChoiceChip('Descending', 'desc'),
              ],
            ),
            const SizedBox(height: 20),
            const Text(
              'Loan Type',
              style: TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.w600,
              ),
            ),
            const SizedBox(height: 12),
            Wrap(
              spacing: 8,
              children: [
                _buildChoiceChip('All Types', 'all'),
                _buildChoiceChip('Personal', 'personal'),
                _buildChoiceChip('Business', 'business'),
                _buildChoiceChip('Agriculture', 'agriculture'),
                _buildChoiceChip('Education', 'education'),
              ],
            ),
            const SizedBox(height: 30),
            SizedBox(
              width: double.infinity,
              child: CustomButton(
                text: 'Apply Filters',
                onPressed: () {
                  _applyAdvancedFilters();
                  Navigator.pop(context);
                },
                style: CustomButtonStyle.primary,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildChoiceChip(String label, String value) {
    bool isSelected = false;
    
    if (label.contains('Application Date') || label.contains('application_date')) {
      isSelected = _selectedSortBy == 'application_date';
    } else if (label.contains('Ascending') || label.contains('asc')) {
      isSelected = _selectedSortOrder == 'asc';
    } else if (label.contains('All Types') || label.contains('all')) {
      isSelected = _selectedLoanType == 'all';
    }

    return ChoiceChip(
      label: Text(label),
      selected: isSelected,
      onSelected: (selected) {
        setState(() {
          if (label.contains('Application Date') || label.contains('application_date')) {
            _selectedSortBy = value;
          } else if (label.contains('Ascending') || label.contains('asc')) {
            _selectedSortOrder = value;
          } else if (label.contains('All Types') || label.contains('all')) {
            _selectedLoanType = value;
          }
        });
      },
      selectedColor: AppTheme.primaryColor.withOpacity(0.2),
      checkmarkColor: AppTheme.primaryColor,
      backgroundColor: Colors.grey[200],
      labelStyle: TextStyle(
        color: isSelected ? AppTheme.primaryColor : Colors.black87,
        fontWeight: isSelected ? FontWeight.w600 : FontWeight.normal,
      ),
    );
  }

  void _applyAdvancedFilters() {
    final provider = context.read<SMLLoanProvider>();
    provider.filterLoans(
      sortBy: _selectedSortBy,
      sortOrder: _selectedSortOrder,
      loanType: _selectedLoanType,
    );
  }

  void _showMoreOptions() {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (context) => _buildMoreOptionsSheet(),
    );
  }

  Widget _buildMoreOptionsSheet() {
    return Container(
      decoration: const BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Text(
                  'More Options',
                  style: TextStyle(
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                IconButton(
                  onPressed: () => Navigator.pop(context),
                  icon: const Icon(Icons.close),
                ),
              ],
            ),
            const SizedBox(height: 20),
            _buildOptionTile(
              'Export Loans',
              Icons.file_download,
              () {
                Navigator.pop(context);
                _exportLoans();
              },
            ),
            _buildOptionTile(
              'Loan Settings',
              Icons.settings,
              () {
                Navigator.pop(context);
                _openLoanSettings();
              },
            ),
            _buildOptionTile(
              'Help & Support',
              Icons.help,
              () {
                Navigator.pop(context);
                _openHelpSupport();
              },
            ),
            _buildOptionTile(
              'About Loans',
              Icons.info,
              () {
                Navigator.pop(context);
                _showAboutLoans();
              },
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildOptionTile(String title, IconData icon, VoidCallback onTap) {
    return ListTile(
      leading: Icon(icon, color: AppTheme.primaryColor),
      title: Text(title),
      onTap: onTap,
      trailing: const Icon(Icons.arrow_forward_ios, size: 16),
    );
  }

  void _exportLoans() {
    // Implement export functionality
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text('Export functionality coming soon!'),
        backgroundColor: AppTheme.infoColor,
      ),
    );
  }

  void _openLoanSettings() {
    // Navigate to loan settings
    Get.toNamed('/loan-settings');
  }

  void _openHelpSupport() {
    // Navigate to help and support
    Get.toNamed('/help-support');
  }

  void _showAboutLoans() {
    // Show about loans dialog
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('About Loan Management'),
        content: const Text(
          'This module provides comprehensive loan management capabilities including application tracking, status monitoring, and document management.',
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('OK'),
          ),
        ],
      ),
    );
  }
}

