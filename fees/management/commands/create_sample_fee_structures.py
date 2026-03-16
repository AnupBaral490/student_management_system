from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from academic.models import Class, AcademicYear
from fees.models import FeeStructure, StudentFee
from accounts.models import StudentProfile


class Command(BaseCommand):
    help = 'Create sample fee structures for all classes'

    def handle(self, *args, **options):
        # Get current academic year
        current_year = AcademicYear.objects.filter(is_current=True).first()
        if not current_year:
            self.stdout.write(self.style.ERROR('No current academic year found. Please create one first.'))
            return

        # Get all classes
        classes = Class.objects.filter(academic_year=current_year)
        if not classes.exists():
            self.stdout.write(self.style.ERROR('No classes found for current academic year.'))
            return

        fee_structures_created = 0
        student_fees_created = 0

        # Define fee structure templates based on year
        fee_templates = {
            1: {
                'tuition_fee': 50000,
                'library_fee': 2000,
                'lab_fee': 3000,
                'sports_fee': 1500,
                'transport_fee': 5000,
                'other_fee': 1000,
            },
            2: {
                'tuition_fee': 55000,
                'library_fee': 2500,
                'lab_fee': 3500,
                'sports_fee': 1500,
                'transport_fee': 5000,
                'other_fee': 1500,
            },
            3: {
                'tuition_fee': 60000,
                'library_fee': 3000,
                'lab_fee': 4000,
                'sports_fee': 2000,
                'transport_fee': 5000,
                'other_fee': 2000,
            },
            4: {
                'tuition_fee': 65000,
                'library_fee': 3500,
                'lab_fee': 4500,
                'sports_fee': 2000,
                'transport_fee': 5000,
                'other_fee': 2500,
            },
        }

        # Create fee structures for each class
        for class_obj in classes:
            year = class_obj.year
            template = fee_templates.get(year, fee_templates[1])

            # Create fee structure for each frequency
            for frequency in ['semester', 'annual']:
                # Calculate due date (15 days from now for semester, 30 days for annual)
                if frequency == 'semester':
                    due_date = timezone.now().date() + timedelta(days=15)
                else:
                    due_date = timezone.now().date() + timedelta(days=30)

                fee_structure, created = FeeStructure.objects.get_or_create(
                    class_assigned=class_obj,
                    academic_year=current_year,
                    frequency=frequency,
                    defaults={
                        'tuition_fee': template['tuition_fee'],
                        'library_fee': template['library_fee'],
                        'lab_fee': template['lab_fee'],
                        'sports_fee': template['sports_fee'],
                        'transport_fee': template['transport_fee'],
                        'other_fee': template['other_fee'],
                        'due_date': due_date,
                        'late_fee_amount': 500,
                        'late_fee_applicable_after_days': 7,
                        'description': f'Fee structure for {class_obj.name} - {frequency.capitalize()}',
                        'is_active': True,
                    }
                )

                if created:
                    fee_structures_created += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'✓ Created fee structure: {class_obj.name} - {frequency.capitalize()}'
                        )
                    )

                    # Create student fees for all students in this class
                    from academic.models import StudentEnrollment
                    enrollments = StudentEnrollment.objects.filter(
                        class_enrolled=class_obj,
                        is_active=True
                    )

                    for enrollment in enrollments:
                        student_fee, sf_created = StudentFee.objects.get_or_create(
                            student=enrollment.student,
                            fee_structure=fee_structure,
                            defaults={
                                'amount_due': fee_structure.total_fee,
                                'amount_paid': 0,
                                'payment_status': 'pending',
                                'remarks': f'Auto-generated for {enrollment.student.user.get_full_name()}',
                            }
                        )

                        if sf_created:
                            student_fees_created += 1

        self.stdout.write('\n' + '='*70)
        self.stdout.write(self.style.SUCCESS(f'✓ Fee structures created: {fee_structures_created}'))
        self.stdout.write(self.style.SUCCESS(f'✓ Student fees created: {student_fees_created}'))
        self.stdout.write('='*70)

        # Show summary
        self.stdout.write('\nFEE STRUCTURE SUMMARY:')
        self.stdout.write('='*70)

        for class_obj in classes:
            structures = FeeStructure.objects.filter(
                class_assigned=class_obj,
                academic_year=current_year
            )
            if structures.exists():
                self.stdout.write(f'\n{class_obj.name}:')
                for fs in structures:
                    self.stdout.write(
                        f'  • {fs.get_frequency_display()}: Rs. {fs.total_fee:,.2f} (Due: {fs.due_date})'
                    )
