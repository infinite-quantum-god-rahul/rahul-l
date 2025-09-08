import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:web_socket_channel/web_socket_channel.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart';

import '../../config/app_theme.dart';
import '../../widgets/common/custom_button.dart';
import '../../widgets/common/custom_text_field.dart';
import '../../widgets/common/loading_overlay.dart';

class RealtimeFeaturesScreen extends StatefulWidget {
  const RealtimeFeaturesScreen({Key? key}) : super(key: key);

  @override
  State<RealtimeFeaturesScreen> createState() => _RealtimeFeaturesScreenState();
}

class _RealtimeFeaturesScreenState extends State<RealtimeFeaturesScreen>
    with TickerProviderStateMixin {
  late AnimationController _animationController;
  late Animation<double> _fadeAnimation;

  final TextEditingController _messageController = TextEditingController();
  bool _isWebSocketConnected = false;
  bool _isNotificationsEnabled = true;
  bool _isLiveChatActive = false;

  List<Map<String, dynamic>> _notifications = [];
  List<Map<String, dynamic>> _chatMessages = [];
  List<Map<String, dynamic>> _liveUpdates = [];

  WebSocketChannel? _webSocketChannel;

  @override
  void initState() {
    super.initState();
    _initializeAnimations();
    _loadSampleData();
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

    _animationController.forward();
  }

  void _loadSampleData() {
    _notifications = [
      {
        'id': 1,
        'title': 'New Loan Application',
        'body': 'Client John Doe submitted a new loan application',
        'timestamp': DateTime.now().subtract(const Duration(minutes: 5)),
        'isRead': false,
      },
      {
        'id': 2,
        'title': 'Payment Received',
        'body': 'Payment of ₹50,000 received from Client ID: C001',
        'timestamp': DateTime.now().subtract(const Duration(minutes: 15)),
        'isRead': true,
      },
    ];

    _chatMessages = [
      {
        'id': 1,
        'sender': 'Support Team',
        'message': 'Hello! How can we help you today?',
        'timestamp': DateTime.now().subtract(const Duration(minutes: 10)),
        'isFromUser': false,
      },
      {
        'id': 2,
        'sender': 'You',
        'message': 'I need help with loan application process',
        'timestamp': DateTime.now().subtract(const Duration(minutes: 8)),
        'isFromUser': true,
      },
    ];

    _liveUpdates = [
      {
        'id': 1,
        'title': 'Loan Status Updated',
        'description': 'Loan L001 status changed from Pending to Approved',
        'timestamp': DateTime.now().subtract(const Duration(minutes: 2)),
      },
      {
        'id': 2,
        'title': 'Payment Processing',
        'description': 'Payment of ₹25,000 is being processed for Client C003',
        'timestamp': DateTime.now().subtract(const Duration(minutes: 5)),
      },
    ];
  }

  @override
  void dispose() {
    _animationController.dispose();
    _messageController.dispose();
    _webSocketChannel?.sink.close();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      length: 3,
      child: Scaffold(
        body: LoadingOverlay(
          isLoading: false,
          child: Column(
            children: [
              _buildTabBar(),
              Expanded(
                child: TabBarView(
                  children: [
                    _buildNotificationsTab(),
                    _buildLiveChatTab(),
                    _buildLiveUpdatesTab(),
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
        tabs: const [
          Tab(icon: Icon(Icons.notifications), text: 'Notifications'),
          Tab(icon: Icon(Icons.chat), text: 'Live Chat'),
          Tab(icon: Icon(Icons.update), text: 'Live Updates'),
        ],
      ),
    );
  }

  Widget _buildNotificationsTab() {
    return CustomScrollView(
      slivers: [
        _buildNotificationsHeader(),
        _buildNotificationsList(),
      ],
    );
  }

  Widget _buildLiveChatTab() {
    return Column(
      children: [
        _buildLiveChatHeader(),
        Expanded(child: _buildChatInterface()),
      ],
    );
  }

  Widget _buildLiveUpdatesTab() {
    return CustomScrollView(
      slivers: [
        _buildLiveUpdatesHeader(),
        _buildLiveUpdatesList(),
      ],
    );
  }

  Widget _buildNotificationsHeader() {
    return SliverAppBar(
      expandedHeight: 120,
      floating: false,
      pinned: true,
      backgroundColor: AppTheme.primaryColor,
      flexibleSpace: FlexibleSpaceBar(
        title: const Text('Notifications', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
        background: Container(
          decoration: BoxDecoration(gradient: AppTheme.primaryGradient),
          child: Padding(
            padding: const EdgeInsets.fromLTRB(16, 60, 16, 16),
            child: Row(
              children: [
                Expanded(child: _buildQuickStat('Total', '${_notifications.length}', Icons.notifications)),
                Expanded(child: _buildQuickStat('Unread', '${_notifications.where((n) => !n['isRead']).length}', Icons.mark_email_unread)),
                Expanded(child: _buildQuickStat('Today', '${_notifications.where((n) => n['timestamp'].day == DateTime.now().day).length}', Icons.today)),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildLiveChatHeader() {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppTheme.secondaryColor,
        gradient: AppTheme.successGradient,
      ),
      child: Row(
        children: [
          CircleAvatar(
            backgroundColor: Colors.white.withOpacity(0.2),
            child: const Icon(Icons.support_agent, color: Colors.white),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text(
                  'Live Chat Support',
                  style: TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold),
                ),
                Text(
                  _isLiveChatActive ? 'Connected' : 'Connecting...',
                  style: TextStyle(color: Colors.white70, fontSize: 14),
                ),
              ],
            ),
          ),
          Switch(
            value: _isLiveChatActive,
            onChanged: _toggleLiveChat,
            activeColor: Colors.white,
            activeTrackColor: Colors.white.withOpacity(0.3),
          ),
        ],
      ),
    );
  }

  Widget _buildLiveUpdatesHeader() {
    return SliverAppBar(
      expandedHeight: 120,
      floating: false,
      pinned: true,
      backgroundColor: AppTheme.accentColor,
      flexibleSpace: FlexibleSpaceBar(
        title: const Text('Live Updates', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
        background: Container(
          decoration: BoxDecoration(gradient: AppTheme.warningGradient),
          child: Padding(
            padding: const EdgeInsets.fromLTRB(16, 60, 16, 16),
            child: Row(
              children: [
                Expanded(child: _buildQuickStat('Updates', '${_liveUpdates.length}', Icons.update)),
                Expanded(child: _buildQuickStat('Real-time', '${_isWebSocketConnected ? 'ON' : 'OFF'}', Icons.wifi)),
                Expanded(child: _buildQuickStat('Last Update', '2m ago', Icons.schedule)),
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

  Widget _buildNotificationsList() {
    return SliverToBoxAdapter(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Recent Notifications', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),
            ListView.builder(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              itemCount: _notifications.length,
              itemBuilder: (context, index) {
                final notification = _notifications[index];
                return _buildNotificationCard(notification);
              },
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildNotificationCard(Map<String, dynamic> notification) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      elevation: notification['isRead'] ? 2 : 4,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: ListTile(
        leading: CircleAvatar(
          backgroundColor: AppTheme.primaryColor.withOpacity(0.1),
          child: Icon(Icons.notifications, color: AppTheme.primaryColor),
        ),
        title: Text(notification['title'], style: TextStyle(fontWeight: notification['isRead'] ? FontWeight.normal : FontWeight.bold)),
        subtitle: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(notification['body']),
            Text(
              _formatTimestamp(notification['timestamp']),
              style: TextStyle(fontSize: 12, color: Colors.grey[600]),
            ),
          ],
        ),
        onTap: () => _markNotificationAsRead(notification),
      ),
    );
  }

  Widget _buildChatInterface() {
    return Column(
      children: [
        Expanded(child: _buildChatMessages()),
        _buildChatInput(),
      ],
    );
  }

  Widget _buildChatMessages() {
    return ListView.builder(
      padding: const EdgeInsets.all(16),
      itemCount: _chatMessages.length,
      itemBuilder: (context, index) {
        final message = _chatMessages[index];
        return _buildChatMessage(message);
      },
    );
  }

  Widget _buildChatMessage(Map<String, dynamic> message) {
    final isFromUser = message['isFromUser'];
    
    return Padding(
      padding: const EdgeInsets.only(bottom: 16),
      child: Row(
        mainAxisAlignment: isFromUser ? MainAxisAlignment.end : MainAxisAlignment.start,
        children: [
          if (!isFromUser) ...[
            CircleAvatar(
              backgroundColor: AppTheme.secondaryColor,
              child: const Text('S', style: TextStyle(color: Colors.white)),
            ),
            const SizedBox(width: 8),
          ],
          Flexible(
            child: Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: isFromUser ? AppTheme.primaryColor : Colors.grey[200],
                borderRadius: BorderRadius.circular(16),
              ),
              child: Text(
                message['message'],
                style: TextStyle(
                  color: isFromUser ? Colors.white : Colors.black87,
                  fontSize: 14,
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildChatInput() {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        boxShadow: [
          BoxShadow(
            color: Colors.grey.withOpacity(0.1),
            spreadRadius: 1,
            blurRadius: 3,
            offset: const Offset(0, -1),
          ),
        ],
      ),
      child: Row(
        children: [
          Expanded(
            child: CustomTextField(
              controller: _messageController,
              hintText: 'Type your message...',
              maxLines: null,
            ),
          ),
          const SizedBox(width: 12),
          IconButton(
            onPressed: _isLiveChatActive ? _sendMessage : null,
            icon: const Icon(Icons.send),
            color: _isLiveChatActive ? AppTheme.primaryColor : Colors.grey,
          ),
        ],
      ),
    );
  }

  Widget _buildLiveUpdatesList() {
    return SliverToBoxAdapter(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Live Updates', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),
            ListView.builder(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              itemCount: _liveUpdates.length,
              itemBuilder: (context, index) {
                final update = _liveUpdates[index];
                return _buildLiveUpdateCard(update);
              },
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildLiveUpdateCard(Map<String, dynamic> update) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      elevation: 3,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: ListTile(
        leading: CircleAvatar(
          backgroundColor: AppTheme.accentColor.withOpacity(0.1),
          child: Icon(Icons.update, color: AppTheme.accentColor),
        ),
        title: Text(update['title'], style: const TextStyle(fontWeight: FontWeight.w600)),
        subtitle: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(update['description']),
            Text(
              _formatTimestamp(update['timestamp']),
              style: TextStyle(fontSize: 12, color: Colors.grey[600]),
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

  String _formatTimestamp(DateTime timestamp) {
    final now = DateTime.now();
    final difference = now.difference(timestamp);
    
    if (difference.inDays > 0) {
      return '${difference.inDays}d ago';
    } else if (difference.inHours > 0) {
      return '${difference.inHours}h ago';
    } else if (difference.inMinutes > 0) {
      return '${difference.inMinutes}m ago';
    } else {
      return 'Just now';
    }
  }

  void _toggleLiveChat(bool value) {
    setState(() {
      _isLiveChatActive = value;
    });
  }

  void _sendMessage() {
    if (_messageController.text.trim().isEmpty) return;

    final newMessage = {
      'id': _chatMessages.length + 1,
      'sender': 'You',
      'message': _messageController.text.trim(),
      'timestamp': DateTime.now(),
      'isFromUser': true,
    };

    setState(() {
      _chatMessages.add(newMessage);
    });

    _messageController.clear();

    // Simulate response
    Future.delayed(const Duration(seconds: 2), () {
      final responseMessage = {
        'id': _chatMessages.length + 1,
        'sender': 'Support Team',
        'message': 'Thank you for your message. We will get back to you shortly.',
        'timestamp': DateTime.now(),
        'isFromUser': false,
      };

      setState(() {
        _chatMessages.add(responseMessage);
      });
    });
  }

  void _markNotificationAsRead(Map<String, dynamic> notification) {
    setState(() {
      notification['isRead'] = !notification['isRead'];
    });
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
            _buildQuickActionTile('Send Notification', Icons.notifications, () { Navigator.pop(context); _sendTestNotification(); }),
            _buildQuickActionTile('Start Chat', Icons.chat, () { Navigator.pop(context); _startNewChat(); }),
            _buildQuickActionTile('Test WebSocket', Icons.wifi, () { Navigator.pop(context); _testWebSocket(); }),
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

  void _sendTestNotification() {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Sending test notification...'), backgroundColor: AppTheme.infoColor),
    );
  }

  void _startNewChat() {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Starting new chat...'), backgroundColor: AppTheme.infoColor),
    );
  }

  void _testWebSocket() {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Testing WebSocket connection...'), backgroundColor: AppTheme.infoColor),
    );
  }
}
