// To clear cache on devices, always increase APP_VER number after making changes.
// The app will serve fresh content right away or after 2-3 refreshes (open / close)
var APP_NAME = 'myPurse';
var APP_VER = '1.1';
var CACHE_NAME = APP_NAME + '-' + APP_VER;

// Files required to make this app work offline.
// Add all files you want to view offline below.
// Leave REQUIRED_FILES = [] to disable offline.
var REQUIRED_FILES = [
	// HTML Files
	'../template/index.html',
	'../template/component-accordions.html',
	'../template/component-actions.html',
	'../template/component-add-to-home.html',
	'../template/component-alerts.html',
	'../template/component-buttons.html',
	'../template/component-cards.html',
	'../template/component-carousels.html',
	'../template/component-charts.html',
	'../template/component-collapse.html',
	'../template/component-colors.html',
	'../template/component-columns.html',
	'../template/component-footer-bar.html',
	'../template/component-grid.html',
	'../template/component-header-bar.html',
	'../template/component-inputs.html',
	'../template/component-list-groups.html',
	'../template/component-menus.html',
	'../template/component-progress.html',
	'../template/component-tables.html',
	'../template/component-tabs.html',
	'../template/component-typography.html',
	'../template/components.html',
	'../template/index-dashboard.html',
	'../template/index-crypto.html',
	'../template/index-waves.html',
	'../template/menu-add-card.html',
	'../template/menu-card-settings.html',
	'../template/menu-exchange.html',
	'../template/menu-friends-transfer.html',
	'../template/menu-highlights.html',
	'../template/menu-notifications.html',
	'../template/menu-request.html',
	'../template/menu-sidebar.html',
	'../template/menu-transfer.html',
	'../template/page-activity.html',
	'../template/page-cards-add.html',
	'../template/page-cards-exchange.html',
	'../template/page-cards-multiple.html',
	'../template/page-cards-single.html',
	'../template/page-crypto-report.html',
	'../template/page-forgot-1.html',
	'../template/page-forgot-2.html',
	'../template/page-goals.html',
	'../template/page-invoice.html',
	'../template/page-payment-bill.html',
	'../template/page-payment-exchange.html',
	'../template/page-payment-request.html',
	'../template/page-payment-transfer.html',
	'../template/page-payments.html',
	'../template/page-profile.html',
	'../template/page-reports.html',
	'../template/page-sign-in.html',
	'../template/page-sign-up.html',
	'../template/page-terms-of-service.html',
	'../template/page-wallet.html',
	'../template/pages.html',
	'../template/walkthrough.html',

	
	'homepageApp/templates/404.html',
	'homepageApp/templates/about.html',
	'homepageApp/templates/contact.html',
	'homepageApp/templates/email_verify.html',
	'homepageApp/templates/index.html',
	'homepageApp/templates/price.html',
	'homepageApp/templates/services.html',
	'homepageApp/templates/signin.html',
	'homepageApp/templates/signup.html',
	'homepageApp/templates/teams.html',



	// Styles
	'styles/style.css',
	'styles/bootstrap.css',
	// Scripts
	'scripts/custom.js',
	'scripts/bootstrap.min.js',
	// Plugins
	'plugins/apex/apexcharts.js',
	'plugins/apex/apex-call.js',
	'plugins/demo/demo.js',
	// Fonts
	'fonts/bootstrap-icons.css',
	'fonts/bootstrap-icons.woff',
	'fonts/bootstrap-icons.woff2',
	// Images
	'images/empty.png',
];

// Service Worker Diagnostic. Set true to get console logs.
var APP_DIAG = false;

//Service Worker Function Below.
self.addEventListener('install', function(event) {
	event.waitUntil(
		caches.open(CACHE_NAME)
		.then(function(cache) {
			//Adding files to cache
			return cache.addAll(REQUIRED_FILES);
		}).catch(function(error) {
			cache.addAll(REQUIRED_FILES);
			//Output error if file locations are incorrect
			if(APP_DIAG){console.log('Service Worker Cache: Error Check REQUIRED_FILES array in _service-worker.js - files are missing or path to files is incorrectly written -  ' + error);}
		})
		.then(function() {
			//Install SW if everything is ok
			return self.skipWaiting();
		})
		.then(function(){
			if(APP_DIAG){console.log('Service Worker: Cache is OK');}
		})
	);
	if(APP_DIAG){console.log('Service Worker: Installed');}
});

self.addEventListener('fetch', function(event) {
	event.respondWith(
		//Fetch Data from cache if offline
		caches.match(event.request)
			.then(function(response) {
				if (response) {return response;}
				return fetch(event.request);
			}
		)
	);
	if(APP_DIAG){console.log('Service Worker: Fetching '+APP_NAME+'-'+APP_VER+' files from Cache');}
});

self.addEventListener('activate', function(event) {
	event.waitUntil(self.clients.claim());
	event.waitUntil(
		//Check cache number, clear all assets and re-add if cache number changed
		caches.keys().then(cacheNames => {
			return Promise.all(
				cacheNames
					.filter(cacheName => (cacheName.startsWith(APP_NAME + "-")))
					.filter(cacheName => (cacheName !== CACHE_NAME))
					.map(cacheName => caches.delete(cacheName))
			);
		})
	);
	if(APP_DIAG){console.log('Service Worker: Activated')}
});