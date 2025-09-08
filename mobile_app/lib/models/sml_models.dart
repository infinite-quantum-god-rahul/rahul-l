import 'package:intl/intl.dart';

// SML Client Model
class SMLClient {
  final int id;
  final String clientCode;
  final String firstName;
  final String lastName;
  final String? middleName;
  final String? email;
  final String? phoneNumber;
  final String? alternatePhone;
  final DateTime? dateOfBirth;
  final String? gender;
  final String? maritalStatus;
  final String? address;
  final String? village;
  final String? center;
  final String? district;
  final String? state;
  final String? pincode;
  final String? aadhaarNumber;
  final String? panNumber;
  final String? occupation;
  final String? monthlyIncome;
  final String? status;
  final DateTime createdAt;
  final DateTime? updatedAt;
  final String? createdBy;
  final String? updatedBy;
  final Map<String, dynamic>? additionalData;

  SMLClient({
    required this.id,
    required this.clientCode,
    required this.firstName,
    required this.lastName,
    this.middleName,
    this.email,
    this.phoneNumber,
    this.alternatePhone,
    this.dateOfBirth,
    this.gender,
    this.maritalStatus,
    this.address,
    this.village,
    this.center,
    this.district,
    this.state,
    this.pincode,
    this.aadhaarNumber,
    this.panNumber,
    this.occupation,
    this.monthlyIncome,
    this.status = 'active',
    required this.createdAt,
    this.updatedAt,
    this.createdBy,
    this.updatedBy,
    this.additionalData,
  });

  String get fullName => '$firstName $lastName'.trim();
  String get displayName => middleName != null ? '$firstName $middleName $lastName' : fullName;
  String get initials => '${firstName[0]}${lastName[0]}'.toUpperCase();
  int get age => dateOfBirth != null ? DateTime.now().difference(dateOfBirth!).inDays ~/ 365 : 0;

  factory SMLClient.fromJson(Map<String, dynamic> json) {
    return SMLClient(
      id: json['id'],
      clientCode: json['client_code'] ?? '',
      firstName: json['first_name'] ?? '',
      lastName: json['last_name'] ?? '',
      middleName: json['middle_name'],
      email: json['email'],
      phoneNumber: json['phone_number'],
      alternatePhone: json['alternate_phone'],
      dateOfBirth: json['date_of_birth'] != null ? DateTime.parse(json['date_of_birth']) : null,
      gender: json['gender'],
      maritalStatus: json['marital_status'],
      address: json['address'],
      village: json['village'],
      center: json['center'],
      district: json['district'],
      state: json['state'],
      pincode: json['pincode'],
      aadhaarNumber: json['aadhaar_number'],
      panNumber: json['pan_number'],
      occupation: json['occupation'],
      monthlyIncome: json['monthly_income'],
      status: json['status'] ?? 'active',
      createdAt: DateTime.parse(json['created_at']),
      updatedAt: json['updated_at'] != null ? DateTime.parse(json['updated_at']) : null,
      createdBy: json['created_by'],
      updatedBy: json['updated_by'],
      additionalData: json['additional_data'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'client_code': clientCode,
      'first_name': firstName,
      'last_name': lastName,
      'middle_name': middleName,
      'email': email,
      'phone_number': phoneNumber,
      'alternate_phone': alternatePhone,
      'date_of_birth': dateOfBirth?.toIso8601String(),
      'gender': gender,
      'marital_status': maritalStatus,
      'address': address,
      'village': village,
      'center': center,
      'district': district,
      'state': state,
      'pincode': pincode,
      'aadhaar_number': aadhaarNumber,
      'pan_number': panNumber,
      'occupation': occupation,
      'monthly_income': monthlyIncome,
      'status': status,
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt?.toIso8601String(),
      'created_by': createdBy,
      'updated_by': updatedBy,
      'additional_data': additionalData,
    };
  }

  SMLClient copyWith({
    int? id,
    String? clientCode,
    String? firstName,
    String? lastName,
    String? middleName,
    String? email,
    String? phoneNumber,
    String? alternatePhone,
    DateTime? dateOfBirth,
    String? gender,
    String? maritalStatus,
    String? address,
    String? village,
    String? center,
    String? district,
    String? state,
    String? pincode,
    String? aadhaarNumber,
    String? panNumber,
    String? occupation,
    String? monthlyIncome,
    String? status,
    DateTime? createdAt,
    DateTime? updatedAt,
    String? createdBy,
    String? updatedBy,
    Map<String, dynamic>? additionalData,
  }) {
    return SMLClient(
      id: id ?? this.id,
      clientCode: clientCode ?? this.clientCode,
      firstName: firstName ?? this.firstName,
      lastName: lastName ?? this.lastName,
      middleName: middleName ?? this.middleName,
      email: email ?? this.email,
      phoneNumber: phoneNumber ?? this.phoneNumber,
      alternatePhone: alternatePhone ?? this.alternatePhone,
      dateOfBirth: dateOfBirth ?? this.dateOfBirth,
      gender: gender ?? this.gender,
      maritalStatus: maritalStatus ?? this.maritalStatus,
      address: address ?? this.address,
      village: village ?? this.village,
      center: center ?? this.center,
      district: district ?? this.district,
      state: state ?? this.state,
      pincode: pincode ?? this.pincode,
      aadhaarNumber: aadhaarNumber ?? this.aadhaarNumber,
      panNumber: panNumber ?? this.panNumber,
      occupation: occupation ?? this.occupation,
      monthlyIncome: monthlyIncome ?? this.monthlyIncome,
      status: status ?? this.status,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
      createdBy: createdBy ?? this.createdBy,
      updatedBy: updatedBy ?? this.updatedBy,
      additionalData: additionalData ?? this.additionalData,
    );
  }

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is SMLClient &&
          runtimeType == other.runtimeType &&
          id == other.id;

  @override
  int get hashCode => id.hashCode;

  @override
  String toString() => 'SMLClient(id: $id, name: $fullName, code: $clientCode)';
}

// SML Loan Application Model
class SMLLoanApplication {
  final int id;
  final String loanCode;
  final int clientId;
  final SMLClient? client;
  final String loanType;
  final double loanAmount;
  final double interestRate;
  final int tenureMonths;
  final String purpose;
  final String status;
  final DateTime applicationDate;
  final DateTime? approvalDate;
  final DateTime? disbursementDate;
  final DateTime? firstEMIDate;
  final double? emiAmount;
  final String? remarks;
  final DateTime createdAt;
  final DateTime? updatedAt;
  final String? createdBy;
  final String? updatedBy;
  final Map<String, dynamic>? additionalData;

  SMLLoanApplication({
    required this.id,
    required this.loanCode,
    required this.clientId,
    this.client,
    required this.loanType,
    required this.loanAmount,
    required this.interestRate,
    required this.tenureMonths,
    required this.purpose,
    this.status = 'pending',
    required this.applicationDate,
    this.approvalDate,
    this.disbursementDate,
    this.firstEMIDate,
    this.emiAmount,
    this.remarks,
    required this.createdAt,
    this.updatedAt,
    this.createdBy,
    this.updatedBy,
    this.additionalData,
  });

  String get formattedLoanAmount => NumberFormat.currency(locale: 'en_IN', symbol: '₹').format(loanAmount);
  String get formattedEMIAmount => emiAmount != null ? NumberFormat.currency(locale: 'en_IN', symbol: '₹').format(emiAmount!) : 'N/A';
  String get formattedApplicationDate => DateFormat('dd MMM yyyy').format(applicationDate);
  bool get isApproved => status == 'approved';
  bool get isDisbursed => status == 'disbursed';
  bool get isActive => status == 'active';

  factory SMLLoanApplication.fromJson(Map<String, dynamic> json) {
    return SMLLoanApplication(
      id: json['id'],
      loanCode: json['loan_code'] ?? '',
      clientId: json['client'],
      client: json['client_details'] != null ? SMLClient.fromJson(json['client_details']) : null,
      loanType: json['loan_type'] ?? '',
      loanAmount: (json['loan_amount'] ?? 0).toDouble(),
      interestRate: (json['interest_rate'] ?? 0).toDouble(),
      tenureMonths: json['tenure_months'] ?? 0,
      purpose: json['purpose'] ?? '',
      status: json['status'] ?? 'pending',
      applicationDate: DateTime.parse(json['application_date']),
      approvalDate: json['approval_date'] != null ? DateTime.parse(json['approval_date']) : null,
      disbursementDate: json['disbursement_date'] != null ? DateTime.parse(json['disbursement_date']) : null,
      firstEMIDate: json['first_emi_date'] != null ? DateTime.parse(json['first_emi_date']) : null,
      emiAmount: json['emi_amount'] != null ? (json['emi_amount']).toDouble() : null,
      remarks: json['remarks'],
      createdAt: DateTime.parse(json['created_at']),
      updatedAt: json['updated_at'] != null ? DateTime.parse(json['updated_at']) : null,
      createdBy: json['created_by'],
      updatedBy: json['updated_by'],
      additionalData: json['additional_data'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'loan_code': loanCode,
      'client': clientId,
      'loan_type': loanType,
      'loan_amount': loanAmount,
      'interest_rate': interestRate,
      'tenure_months': tenureMonths,
      'purpose': purpose,
      'status': status,
      'application_date': applicationDate.toIso8601String(),
      'approval_date': approvalDate?.toIso8601String(),
      'disbursement_date': disbursementDate?.toIso8601String(),
      'first_emi_date': firstEMIDate?.toIso8601String(),
      'emi_amount': emiAmount,
      'remarks': remarks,
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt?.toIso8601String(),
      'created_by': createdBy,
      'updated_by': updatedBy,
      'additional_data': additionalData,
    };
  }

  SMLLoanApplication copyWith({
    int? id,
    String? loanCode,
    int? clientId,
    SMLClient? client,
    String? loanType,
    double? loanAmount,
    double? interestRate,
    int? tenureMonths,
    String? purpose,
    String? status,
    DateTime? applicationDate,
    DateTime? approvalDate,
    DateTime? disbursementDate,
    DateTime? firstEMIDate,
    double? emiAmount,
    String? remarks,
    DateTime? createdAt,
    DateTime? updatedAt,
    String? createdBy,
    String? updatedBy,
    Map<String, dynamic>? additionalData,
  }) {
    return SMLLoanApplication(
      id: id ?? this.id,
      loanCode: loanCode ?? this.loanCode,
      clientId: clientId ?? this.clientId,
      client: client ?? this.client,
      loanType: loanType ?? this.loanType,
      loanAmount: loanAmount ?? this.loanAmount,
      interestRate: interestRate ?? this.interestRate,
      tenureMonths: tenureMonths ?? this.tenureMonths,
      purpose: purpose ?? this.purpose,
      status: status ?? this.status,
      applicationDate: applicationDate ?? this.applicationDate,
      approvalDate: approvalDate ?? this.approvalDate,
      disbursementDate: disbursementDate ?? this.disbursementDate,
      firstEMIDate: firstEMIDate ?? this.firstEMIDate,
      emiAmount: emiAmount ?? this.emiAmount,
      remarks: remarks ?? this.remarks,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
      createdBy: createdBy ?? this.createdBy,
      updatedBy: updatedBy ?? this.updatedBy,
      additionalData: additionalData ?? this.additionalData,
    );
  }

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is SMLLoanApplication &&
          runtimeType == other.runtimeType &&
          id == other.id;

  @override
  int get hashCode => id.hashCode;

  @override
  String toString() => 'SMLLoanApplication(id: $id, code: $loanCode, amount: $formattedLoanAmount)';
}

// SML Field Visit Model
class SMLFieldVisit {
  final int id;
  final String visitCode;
  final int clientId;
  final SMLClient? client;
  final int? loanId;
  final SMLLoanApplication? loan;
  final String visitType;
  final String purpose;
  final String status;
  final String priority;
  final DateTime scheduledDate;
  final DateTime? actualDate;
  final String? location;
  final double? latitude;
  final double? longitude;
  final String? findings;
  final String? recommendations;
  final String? remarks;
  final DateTime createdAt;
  final DateTime? updatedAt;
  final String? createdBy;
  final String? updatedBy;
  final Map<String, dynamic>? additionalData;

  SMLFieldVisit({
    required this.id,
    required this.visitCode,
    required this.clientId,
    this.client,
    this.loanId,
    this.loan,
    required this.visitType,
    required this.purpose,
    this.status = 'scheduled',
    this.priority = 'medium',
    required this.scheduledDate,
    this.actualDate,
    this.location,
    this.latitude,
    this.longitude,
    this.findings,
    this.recommendations,
    this.remarks,
    required this.createdAt,
    this.updatedAt,
    this.createdBy,
    this.updatedBy,
    this.additionalData,
  });

  String get formattedScheduledDate => DateFormat('dd MMM yyyy').format(scheduledDate);
  String get formattedActualDate => actualDate != null ? DateFormat('dd MMM yyyy').format(actualDate!) : 'N/A';
  bool get isCompleted => status == 'completed';
  bool get isOverdue => scheduledDate.isBefore(DateTime.now()) && !isCompleted;
  bool get isToday => DateFormat('yyyy-MM-dd').format(scheduledDate) == DateFormat('yyyy-MM-dd').format(DateTime.now());

  factory SMLFieldVisit.fromJson(Map<String, dynamic> json) {
    return SMLFieldVisit(
      id: json['id'],
      visitCode: json['visit_code'] ?? '',
      clientId: json['client'],
      client: json['client_details'] != null ? SMLClient.fromJson(json['client_details']) : null,
      loanId: json['loan'],
      loan: json['loan_details'] != null ? SMLLoanApplication.fromJson(json['loan_details']) : null,
      visitType: json['visit_type'] ?? '',
      purpose: json['purpose'] ?? '',
      status: json['status'] ?? 'scheduled',
      priority: json['priority'] ?? 'medium',
      scheduledDate: DateTime.parse(json['scheduled_date']),
      actualDate: json['actual_date'] != null ? DateTime.parse(json['actual_date']) : null,
      location: json['location'],
      latitude: json['latitude'] != null ? (json['latitude']).toDouble() : null,
      longitude: json['longitude'] != null ? (json['longitude']).toDouble() : null,
      findings: json['findings'],
      recommendations: json['recommendations'],
      remarks: json['remarks'],
      createdAt: DateTime.parse(json['created_at']),
      updatedAt: json['updated_at'] != null ? DateTime.parse(json['updated_at']) : null,
      createdBy: json['created_by'],
      updatedBy: json['updated_by'],
      additionalData: json['additional_data'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'visit_code': visitCode,
      'client': clientId,
      'loan': loanId,
      'visit_type': visitType,
      'purpose': purpose,
      'status': status,
      'priority': priority,
      'scheduled_date': scheduledDate.toIso8601String(),
      'actual_date': actualDate?.toIso8601String(),
      'location': location,
      'latitude': latitude,
      'longitude': longitude,
      'findings': findings,
      'recommendations': recommendations,
      'remarks': remarks,
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt?.toIso8601String(),
      'created_by': createdBy,
      'updated_by': updatedBy,
      'additional_data': additionalData,
    };
  }

  SMLFieldVisit copyWith({
    int? id,
    String? visitCode,
    int? clientId,
    SMLClient? client,
    int? loanId,
    SMLLoanApplication? loan,
    String? visitType,
    String? purpose,
    String? status,
    String? priority,
    DateTime? scheduledDate,
    DateTime? actualDate,
    String? location,
    double? latitude,
    double? longitude,
    String? findings,
    String? recommendations,
    String? remarks,
    DateTime? createdAt,
    DateTime? updatedAt,
    String? createdBy,
    String? updatedBy,
    Map<String, dynamic>? additionalData,
  }) {
    return SMLFieldVisit(
      id: id ?? this.id,
      visitCode: visitCode ?? this.visitCode,
      clientId: clientId ?? this.clientId,
      client: client ?? this.client,
      loanId: loanId ?? this.loanId,
      loan: loan ?? this.loan,
      visitType: visitType ?? this.visitType,
      purpose: purpose ?? this.purpose,
      status: status ?? this.status,
      priority: priority ?? this.priority,
      scheduledDate: scheduledDate ?? this.scheduledDate,
      actualDate: actualDate ?? this.actualDate,
      location: location ?? this.location,
      latitude: latitude ?? this.latitude,
      longitude: longitude ?? this.longitude,
      findings: findings ?? this.findings,
      recommendations: recommendations ?? this.recommendations,
      remarks: remarks ?? this.remarks,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
      createdBy: createdBy ?? this.createdBy,
      updatedBy: updatedBy ?? this.updatedBy,
      additionalData: additionalData ?? this.additionalData,
    );
  }

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is SMLFieldVisit &&
          runtimeType == other.runtimeType &&
          id == other.id;

  @override
  int get hashCode => id.hashCode;

  @override
  String toString() => 'SMLFieldVisit(id: $id, code: $visitCode, date: $formattedScheduledDate)';
}

// SML Field Schedule Model
class SMLFieldSchedule {
  final int id;
  final String scheduleCode;
  final int clientId;
  final SMLClient? client;
  final int? loanId;
  final SMLLoanApplication? loan;
  final String scheduleType;
  final String purpose;
  final String status;
  final String priority;
  final DateTime scheduledDate;
  final TimeOfDay scheduledTime;
  final String? location;
  final double? latitude;
  final double? longitude;
  final String? notes;
  final DateTime createdAt;
  final DateTime? updatedAt;
  final String? createdBy;
  final String? updatedBy;
  final Map<String, dynamic>? additionalData;

  SMLFieldSchedule({
    required this.id,
    required this.scheduleCode,
    required this.clientId,
    this.client,
    this.loanId,
    this.loan,
    required this.scheduleType,
    required this.purpose,
    this.status = 'scheduled',
    this.priority = 'medium',
    required this.scheduledDate,
    required this.scheduledTime,
    this.location,
    this.latitude,
    this.longitude,
    this.notes,
    required this.createdAt,
    this.updatedAt,
    this.createdBy,
    this.updatedBy,
    this.additionalData,
  });

  String get formattedScheduledDate => DateFormat('dd MMM yyyy').format(scheduledDate);
  String get formattedScheduledTime => scheduledTime.format(null);
  bool get isCompleted => status == 'completed';
  bool get isOverdue => scheduledDate.isBefore(DateTime.now()) && !isCompleted;
  bool get isToday => DateFormat('yyyy-MM-dd').format(scheduledDate) == DateFormat('yyyy-MM-dd').format(DateTime.now());

  factory SMLFieldSchedule.fromJson(Map<String, dynamic> json) {
    final timeStr = json['scheduled_time'] ?? '09:00';
    final timeParts = timeStr.split(':');
    final time = TimeOfDay(
      hour: int.parse(timeParts[0]),
      minute: int.parse(timeParts[1]),
    );

    return SMLFieldSchedule(
      id: json['id'],
      scheduleCode: json['schedule_code'] ?? '',
      clientId: json['client'],
      client: json['client_details'] != null ? SMLClient.fromJson(json['client_details']) : null,
      loanId: json['loan'],
      loan: json['loan_details'] != null ? SMLLoanApplication.fromJson(json['loan_details']) : null,
      scheduleType: json['schedule_type'] ?? '',
      purpose: json['purpose'] ?? '',
      status: json['status'] ?? 'scheduled',
      priority: json['priority'] ?? 'medium',
      scheduledDate: DateTime.parse(json['scheduled_date']),
      scheduledTime: time,
      location: json['location'],
      latitude: json['latitude'] != null ? (json['latitude']).toDouble() : null,
      longitude: json['longitude'] != null ? (json['longitude']).toDouble() : null,
      notes: json['notes'],
      createdAt: DateTime.parse(json['created_at']),
      updatedAt: json['updated_at'] != null ? DateTime.parse(json['updated_at']) : null,
      createdBy: json['created_by'],
      updatedBy: json['updated_by'],
      additionalData: json['additional_data'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'schedule_code': scheduleCode,
      'client': clientId,
      'loan': loanId,
      'schedule_type': scheduleType,
      'purpose': purpose,
      'status': status,
      'priority': priority,
      'scheduled_date': scheduledDate.toIso8601String(),
      'scheduled_time': '${scheduledTime.hour.toString().padLeft(2, '0')}:${scheduledTime.minute.toString().padLeft(2, '0')}',
      'location': location,
      'latitude': latitude,
      'longitude': longitude,
      'notes': notes,
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt?.toIso8601String(),
      'created_by': createdBy,
      'updated_by': updatedBy,
      'additional_data': additionalData,
    };
  }

  SMLFieldSchedule copyWith({
    int? id,
    String? scheduleCode,
    int? clientId,
    SMLClient? client,
    int? loanId,
    SMLLoanApplication? loan,
    String? scheduleType,
    String? purpose,
    String? status,
    String? priority,
    DateTime? scheduledDate,
    TimeOfDay? scheduledTime,
    String? location,
    double? latitude,
    double? longitude,
    String? notes,
    DateTime? createdAt,
    DateTime? updatedAt,
    String? createdBy,
    String? updatedBy,
    Map<String, dynamic>? additionalData,
  }) {
    return SMLFieldSchedule(
      id: id ?? this.id,
      scheduleCode: scheduleCode ?? this.scheduleCode,
      clientId: clientId ?? this.clientId,
      client: client ?? this.client,
      loanId: loanId ?? this.loanId,
      loan: loan ?? this.loan,
      scheduleType: scheduleType ?? this.scheduleType,
      purpose: purpose ?? this.purpose,
      status: status ?? this.status,
      priority: priority ?? this.priority,
      scheduledDate: scheduledDate ?? this.scheduledDate,
      scheduledTime: scheduledTime ?? this.scheduledTime,
      location: location ?? this.location,
      latitude: latitude ?? this.latitude,
      longitude: longitude ?? this.longitude,
      notes: notes ?? this.notes,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
      createdBy: createdBy ?? this.createdBy,
      updatedBy: updatedBy ?? this.updatedBy,
      additionalData: additionalData ?? this.additionalData,
    );
  }

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is SMLFieldSchedule &&
          runtimeType == other.runtimeType &&
          id == other.id;

  @override
  int get hashCode => id.hashCode;

  @override
  String toString() => 'SMLFieldSchedule(id: $id, code: $scheduleCode, date: $formattedScheduledDate)';
}

// SML KYC Document Model
class SMLKYCDocument {
  final int id;
  final String documentCode;
  final int clientId;
  final SMLClient? client;
  final String documentType;
  final String documentNumber;
  final String fileName;
  final String filePath;
  final String fileSize;
  final String fileType;
  final String status;
  final String? description;
  final DateTime? expiryDate;
  final DateTime uploadedDate;
  final DateTime? verifiedDate;
  final String? verifiedBy;
  final String? remarks;
  final DateTime createdAt;
  final DateTime? updatedAt;
  final String? createdBy;
  final String? updatedBy;
  final Map<String, dynamic>? additionalData;

  SMLKYCDocument({
    required this.id,
    required this.documentCode,
    required this.clientId,
    this.client,
    required this.documentType,
    required this.documentNumber,
    required this.fileName,
    required this.filePath,
    required this.fileSize,
    required this.fileType,
    this.status = 'pending',
    this.description,
    this.expiryDate,
    required this.uploadedDate,
    this.verifiedDate,
    this.verifiedBy,
    this.remarks,
    required this.createdAt,
    this.updatedAt,
    this.createdBy,
    this.updatedBy,
    this.additionalData,
  });

  String get formattedUploadDate => DateFormat('dd MMM yyyy').format(uploadedDate);
  String get formattedExpiryDate => expiryDate != null ? DateFormat('dd MMM yyyy').format(expiryDate!) : 'N/A';
  bool get isVerified => status == 'verified';
  bool get isExpired => expiryDate != null && expiryDate!.isBefore(DateTime.now());
  bool get isExpiringSoon => expiryDate != null && 
      expiryDate!.difference(DateTime.now()).inDays <= 30 && 
      expiryDate!.isAfter(DateTime.now());

  factory SMLKYCDocument.fromJson(Map<String, dynamic> json) {
    return SMLKYCDocument(
      id: json['id'],
      documentCode: json['document_code'] ?? '',
      clientId: json['client'],
      client: json['client_details'] != null ? SMLClient.fromJson(json['client_details']) : null,
      documentType: json['document_type'] ?? '',
      documentNumber: json['document_number'] ?? '',
      fileName: json['file_name'] ?? '',
      filePath: json['file_path'] ?? '',
      fileSize: json['file_size'] ?? '',
      fileType: json['file_type'] ?? '',
      status: json['status'] ?? 'pending',
      description: json['description'],
      expiryDate: json['expiry_date'] != null ? DateTime.parse(json['expiry_date']) : null,
      uploadedDate: DateTime.parse(json['uploaded_date']),
      verifiedDate: json['verified_date'] != null ? DateTime.parse(json['verified_date']) : null,
      verifiedBy: json['verified_by'],
      remarks: json['remarks'],
      createdAt: DateTime.parse(json['created_at']),
      updatedAt: json['updated_at'] != null ? DateTime.parse(json['updated_at']) : null,
      createdBy: json['created_by'],
      updatedBy: json['updated_by'],
      additionalData: json['additional_data'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'document_code': documentCode,
      'client': clientId,
      'document_type': documentType,
      'document_number': documentNumber,
      'file_name': fileName,
      'file_path': filePath,
      'file_size': fileSize,
      'file_type': fileType,
      'status': status,
      'description': description,
      'expiry_date': expiryDate?.toIso8601String(),
      'uploaded_date': uploadedDate.toIso8601String(),
      'verified_date': verifiedDate?.toIso8601String(),
      'verified_by': verifiedBy,
      'remarks': remarks,
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt?.toIso8601String(),
      'created_by': createdBy,
      'updated_by': updatedBy,
      'additional_data': additionalData,
    };
  }

  SMLKYCDocument copyWith({
    int? id,
    String? documentCode,
    int? clientId,
    SMLClient? client,
    String? documentType,
    String? documentNumber,
    String? fileName,
    String? filePath,
    String? fileSize,
    String? fileType,
    String? status,
    String? description,
    DateTime? expiryDate,
    DateTime? uploadedDate,
    DateTime? verifiedDate,
    String? verifiedBy,
    String? remarks,
    DateTime? createdAt,
    DateTime? updatedAt,
    String? createdBy,
    String? updatedBy,
    Map<String, dynamic>? additionalData,
  }) {
    return SMLKYCDocument(
      id: id ?? this.id,
      documentCode: documentCode ?? this.documentCode,
      clientId: clientId ?? this.clientId,
      client: client ?? this.client,
      documentType: documentType ?? this.documentType,
      documentNumber: documentNumber ?? this.documentNumber,
      fileName: fileName ?? this.fileName,
      filePath: filePath ?? this.filePath,
      fileSize: fileSize ?? this.fileSize,
      fileType: fileType ?? this.fileType,
      status: status ?? this.status,
      description: description ?? this.description,
      expiryDate: expiryDate ?? this.expiryDate,
      uploadedDate: uploadedDate ?? this.uploadedDate,
      verifiedDate: verifiedDate ?? this.verifiedDate,
      verifiedBy: verifiedBy ?? this.verifiedBy,
      remarks: remarks ?? this.remarks,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
      createdBy: createdBy ?? this.createdBy,
      updatedBy: updatedBy ?? this.updatedBy,
      additionalData: additionalData ?? this.additionalData,
    );
  }

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is SMLKYCDocument &&
          runtimeType == other.runtimeType &&
          id == other.id;

  @override
  int get hashCode => id.hashCode;

  @override
  String toString() => 'SMLKYCDocument(id: $id, type: $documentType, number: $documentNumber)';
}

// TimeOfDay extension for JSON serialization
class TimeOfDay {
  final int hour;
  final int minute;

  const TimeOfDay({required this.hour, required this.minute});

  String format(BuildContext? context) {
    final hour = this.hour.toString().padLeft(2, '0');
    final minute = this.minute.toString().padLeft(2, '0');
    return '$hour:$minute';
  }

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is TimeOfDay &&
          runtimeType == other.runtimeType &&
          hour == other.hour &&
          minute == other.minute;

  @override
  int get hashCode => hour.hashCode ^ minute.hashCode;
}

