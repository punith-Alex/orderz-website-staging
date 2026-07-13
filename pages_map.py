"""Map docx stems to URLs, page-type labels, and breadcrumbs."""

# (stem, url, eyebrow, crumbs) — crumbs: list of (label, url-or-None)
SUB = lambda label, hub, huburl: dict(eyebrow=label + " · Singapore", crumbs=[(hub, huburl), (label, None)])
POS = lambda label, hub, huburl: dict(eyebrow="POS System · " + label, crumbs=[(hub, huburl), (label + " POS", None)])
SOL = lambda label: dict(eyebrow="Solution · " + label, crumbs=[("Solutions", None), (label, None)])
UC  = lambda label: dict(eyebrow="Use Case · " + label, crumbs=[("Use Cases", None), (label, None)])
HUB = lambda label: dict(eyebrow=label + " Industry Hub · Singapore", crumbs=[(label, None)])
CORE = lambda label: dict(eyebrow="OrderZ · " + label, crumbs=[(label, None)])
ECOM = lambda label: dict(eyebrow="eCommerce Builder · " + label, crumbs=[("eCommerce Builder", "ecommerce-builder/"), (label, None)])

PAGES_MAP = {
  # ---- FnB sub-category 360 pages ----
  "OrderZ_Restaurants_Sub_Page_Copy":   ("restaurants/", SUB("Restaurants", "Food & Beverage", "fnb/")),
  "OrderZ_Hawker_Stalls_Page_Copy":     ("hawker-stalls/", SUB("Hawker Stalls", "Food & Beverage", "fnb/")),
  "OrderZ_Food_Courts_Page_Copy":       ("food-courts/", SUB("Food Courts", "Food & Beverage", "fnb/")),
  "OrderZ_QSR_Page_Copy":               ("qsr/", SUB("QSR & Fast Food", "Food & Beverage", "fnb/")),
  "OrderZ_Casual_Dining_Page_Copy":     ("casual-dining/", SUB("Casual Dining", "Food & Beverage", "fnb/")),
  "OrderZ_Small_Chains_Page_Copy":      ("small-chains/", SUB("Small Chains", "Food & Beverage", "fnb/")),
  "OrderZ_Bars_Pubs_Page_Copy":         ("bars-pubs/", SUB("Bars & Pubs", "Food & Beverage", "fnb/")),
  # ---- Beautycare sub-category ----
  "OrderZ_HairSalons_Page_Copy":        ("hair-salons/", SUB("Hair Salons", "Beautycare", "beautycare/")),
  "OrderZ_Beauty_Salons_Page_Copy":     ("beauty-salons/", SUB("Beauty Salons", "Beautycare", "beautycare/")),
  "OrderZ_Spas_Page_Copy":              ("spas/", SUB("Spas", "Beautycare", "beautycare/")),
  "OrderZ_NailStudios_Page_Copy":       ("nail-studios/", SUB("Nail Studios", "Beautycare", "beautycare/")),
  "OrderZ_Multi_Branch_Salons_Page_Copy": ("multi-branch-salons/", SUB("Multi-Branch Salons", "Beautycare", "beautycare/")),
  # ---- Wellness sub-category ----
  "OrderZ_Aesthetic_Clinics_Page_Copy": ("aesthetic-clinics/", SUB("Aesthetic Clinics", "Wellness", "wellness/")),
  "OrderZ_Therapy_Centres_Page_Copy":   ("therapy-centres/", SUB("Therapy Centres", "Wellness", "wellness/")),
  "OrderZ_Multi_Branch_Clinics_Page_Copy": ("multi-branch-clinics/", SUB("Multi-Branch Clinics", "Wellness", "wellness/")),
  # ---- POS entry pages ----
  "OrderZ_Restaurants_POS_Page_Copy":   ("restaurants-pos/", POS("Restaurants", "Food & Beverage", "fnb/")),
  "OrderZ_HawkerStalls_POS_Page_Copy":  ("hawker-stalls-pos/", POS("Hawker Stalls", "Food & Beverage", "fnb/")),
  "OrderZ_Cafes_POS_Page_Copy":         ("cafes-pos/", POS("Cafes", "Food & Beverage", "fnb/")),
  "OrderZ_FoodCourts_POS_Page_Copy":    ("food-courts-pos/", POS("Food Courts", "Food & Beverage", "fnb/")),
  "OrderZ_QSR_POS_Page_Copy":           ("qsr-pos/", POS("QSR", "Food & Beverage", "fnb/")),
  "OrderZ_CasualDining_POS_Page_Copy":  ("casual-dining-pos/", POS("Casual Dining", "Food & Beverage", "fnb/")),
  "OrderZ_SmallChains_POS_Page_Copy":   ("small-chains-pos/", POS("Small Chains", "Food & Beverage", "fnb/")),
  "OrderZ_BarsPubs_POS_Page_Copy":      ("bars-pubs-pos/", POS("Bars & Pubs", "Food & Beverage", "fnb/")),
  "OrderZ_HairSalons_POS_Page_Copy":    ("hair-salons-pos/", POS("Hair Salons", "Beautycare", "beautycare/")),
  "OrderZ_BeautySalons_POS_Page_Copy":  ("beauty-salons-pos/", POS("Beauty Salons", "Beautycare", "beautycare/")),
  "OrderZ_Spas_POS_Page_Copy":          ("spas-pos/", POS("Spas", "Beautycare", "beautycare/")),
  "OrderZ_NailStudios_POS_Page_Copy":   ("nail-studios-pos/", POS("Nail Studios", "Beautycare", "beautycare/")),
  "OrderZ_MultiBranchSalons_POS_Page_Copy": ("multi-branch-salons-pos/", POS("Multi-Branch Salons", "Beautycare", "beautycare/")),
  "OrderZ_AestheticClinics_POS_Page_Copy": ("aesthetic-clinics-pos/", POS("Aesthetic Clinics", "Wellness", "wellness/")),
  "OrderZ_TherapyCentres_POS_Page_Copy": ("therapy-centres-pos/", POS("Therapy Centres", "Wellness", "wellness/")),
  "OrderZ_MultiBranchClinics_POS_Page_Copy": ("multi-branch-clinics-pos/", POS("Multi-Branch Clinics", "Wellness", "wellness/")),
  "OrderZ_GeneralRetail_POS_Page_Copy": ("general-retail-pos/", POS("General Retail", "Retail", "retail/")),
  "OrderZ_Minimart_POS_Page_Copy":      ("minimart-pos/", POS("Minimarts", "Retail", "retail/")),
  "OrderZ_FashionApparel_POS_Page_Copy": ("fashion-apparel-pos/", POS("Fashion & Apparel", "Retail", "retail/")),
  "OrderZ_HealthPharmacy_POS_Page_Copy": ("health-pharmacy-pos/", POS("Health & Pharmacy", "Retail", "retail/")),
  "OrderZ_MultiBranchRetail_POS_Page_Copy": ("multi-branch-retail-pos/", POS("Multi-Branch Retail", "Retail", "retail/")),
  # ---- Solutions ----
  "OrderZ_POS_Billing_Page_Copy":       ("pos-billing-system/", SOL("POS & Billing")),
  "OrderZ_Appt_Booking_Page_Copy":      ("appointment-booking-system/", SOL("Appointment Booking")),
  "OrderZ_Online_Ordering_Page_Copy":   ("online-ordering-system/", SOL("Online Ordering")),
  "OrderZ_CRM_Page_Copy":               ("customer-management-crm/", SOL("Customer CRM")),
  "OrderZ_Inventory_Page_Copy":         ("inventory-management/", SOL("Inventory Management")),
  "OrderZ_Reporting_Page_Copy":         ("reporting-analytics/", SOL("Reporting & Analytics")),
  "OrderZ_MultiOutlet_Mgmt_Page_Copy":  ("multi-outlet-management/", SOL("Multi-Outlet Management")),
  "OrderZ_Website_Builder_Page_Copy":   ("website-online-store-builder/", SOL("Website & Online Store Builder")),
  "OrderZ_Payment_Page_Copy":           ("payment-integration/", SOL("Payment Integration")),
  "OrderZ_Workflow_Page_Copy":          ("workflow-operations-management/", SOL("Workflow & Operations")),
  # ---- Use cases ----
  "OrderZ_Speed_Up_Ordering_Page_Copy": ("speed-up-ordering/", UC("Speed Up Order Taking")),
  "OrderZ_Peak_Hours_Page_Copy":        ("peak-hours/", UC("Handle Peak Hour Rush")),
  "OrderZ_Reduce_Order_Errors_Page_Copy": ("reduce-order-errors/", UC("Reduce Order Errors")),
  "OrderZ_Dine_In_Takeaway_Page_Copy":  ("dine-in-takeaway/", UC("Manage Dine-In & Takeaway")),
  "OrderZ_Reduce_Missed_Appointments_Page_Copy": ("reduce-missed-appointments/", UC("Reduce Missed Appointments")),
  "OrderZ_Simplify_Booking_Page_Copy":  ("simplify-booking/", UC("Simplify Booking & Scheduling")),
  "OrderZ_Billing_Accuracy_Page_Copy":  ("billing-accuracy/", UC("Improve Billing Accuracy")),
  "OrderZ_Multi_Outlet_Page_Copy":      ("multi-outlet/", UC("Manage Multiple Outlets")),
  "OrderZ_Customer_Retention_Page_Copy": ("customer-retention/", UC("Improve Customer Retention")),
  # ---- Hubs ----
  "OrderZ_Beautycare_Hub_Page_Copy":    ("beautycare/", HUB("Beautycare")),
  "OrderZ_Wellness_Hub_Page_Copy":      ("wellness/", HUB("Wellness")),
  "OrderZ_Retail_Hub_Page_Copy":        ("retail/", HUB("Retail")),
  "OrderZ_eCommerce_Hub_Page_Copy":     ("ecommerce-builder/", HUB("eCommerce Builder")),
  # ---- eCommerce sub-pages ----
  "OrderZ_RestaurantOnlineStore_Page_Copy": ("restaurant-online-store/", ECOM("Restaurant Online Store")),
  "OrderZ_BeautyOnlineStore_Page_Copy": ("beauty-online-store/", ECOM("Beauty Online Store")),
  "OrderZ_RetailOnlineStore_Page_Copy": ("retail-online-store/", ECOM("Retail Online Store")),
  "OrderZ_HomeBasedBusiness_Page_Copy": ("home-based-business/", ECOM("Home-Based Business")),
  # ---- Core pages ----
  "OrderZ_Platform_Page_Copy":          ("platform/", CORE("Platform Overview")),
  "OrderZ_How_It_Works_Page_Copy":      ("how-it-works/", CORE("How It Works")),
  "OrderZ_Pricing_Page_Copy":           ("pricing/", CORE("Pricing")),
  "OrderZ_Success_Stories_Page_Copy":   ("success-stories/", CORE("Success Stories")),
  "OrderZ_Why_OrderZ_Page_Copy":        ("why-orderz/", CORE("Why OrderZ")),
  "OrderZ_Book_Demo_Page_Copy":         ("book-demo/", CORE("Book a Free Demo")),
  "OrderZ_Contact_Page_Copy":           ("contact/", CORE("Contact")),
  "OrderZ_Support_Page_Copy":           ("support/", CORE("Support")),
  "OrderZ_FAQ_Page_Copy":               ("faq/", CORE("FAQ")),
  "OrderZ_Help_Page_Copy":              ("help/", CORE("Help Centre")),
  "OrderZ_Onboarding_Page_Copy":        ("onboarding/", CORE("Onboarding")),
}

REDIRECTS = [
  ("/industries/restaurants", "/fnb"),
  ("/spa-salon", "/beautycare"),
  ("/industries/spa-salon", "/beautycare"),
  ("/wellness-clinics", "/wellness"),
  ("/wellness-centres", "/wellness"),
  ("/industries/wellness-clinics", "/wellness"),
  ("/pos-billing", "/solutions/pos-billing-system"),
  ("/qr-ordering", "/solutions/qr-ordering-system"),
  ("/appointment-booking", "/solutions/appointment-booking-system"),
  ("/online-ordering", "/solutions/online-ordering-system"),
  ("/crm", "/solutions/customer-management-crm"),
  ("/inventory", "/solutions/inventory-management"),
  ("/reporting", "/solutions/reporting-analytics"),
  ("/multi-outlet-management", "/solutions/multi-outlet-management"),
  ("/website-builder", "/solutions/website-online-store-builder"),
  ("/payment", "/solutions/payment-integration"),
  ("/workflow", "/solutions/workflow-operations-management"),
]
