<script>

export default {

	props: ['user'],
	data() {

		return {

			loggedinUser: {},

			linkList: [

				{ icon: '<i class="material-icons" aria-hidden="true">dashboard</i>', title: 'Dashboard', link: '/#', active: true },
				{ icon: '<i class="material-icons" aria-hidden="true">people</i>', title: 'Fit a Model', link: '/buildModel', active: false }
			],

			forAdmin: [
				{ icon: '<i class="material-icons" aria-hidden="true">dashboard</i>', title: 'Departments', link: '/#', active: false },
				{ icon: '<i class="material-icons" aria-hidden="true">people</i>', title: 'Employees', link: '/buildModel', active: false },
				{ icon: '<i class="material-icons" aria-hidden="true">note_add</i>', title: 'Roles ', link: '/#', active: false }

			],


			logo: 'Machine learning',
			sidebarH: '',

		}
	},

	mounted() {

		this.$nextTick(function () {

			this.sidebarH = this.$parent.$refs.contentwrapper.offsetHeight;

			window.addEventListener('resize', this.resizeSidebar);

			this.getUser();


		})



	},


	methods: {


		getUser() {

			// axios.get(`api/user/${this.user}`).
			// then(response => {
			// 	console.log(response)
			// 	this.loggedinUser = response.data[0].fields
			// })
		},

		resizeSidebar() {

			this.sidebarH = this.sidebarH = this.$parent.$refs.contentwrapper.offsetHeight;
		},


		/*
		*  Change the active state of clicked link
		*
		*/

		changeActive(title) {

			this.linkList = _.map(this.linkList, link => {

				if (link.title == title) {

					link.active = true;
				}
				else {
					link.active = false;
				}

				return link;

			});
		}

	},


	computed: {

		sidebarHeight() {

			// return this.sidebarH + 60;			

		}
	}

}

</script> 


<template>
	<div class="side-nav"
	     ref="sidebar">
	
		<div class="logo">
			<i class="fa fa-tachometer"></i>
			<span> {{ logo }} </span>
		</div>
	
		<nav class="side-list">
	
			<div style="height: 80px; background: #1F60C1; padding-top: 10px;">
	
				<center>
					<img style="border: 2px solid lightgrey; padding: 2px; margin-right: 7px; height: 55px; width: 55px; border-radius: 50%; background: #E9E8E8;"
					     src="/static/img/prof.jpg"
					     class="user-image"
					     alt="User Image" />
				</center>
	
			</div>
	
			<ul v-for="item in linkList">
	
				<li :class="{ active: item.active }">
	
					<a :href="item.link"
					   @click="changeActive(item.title)">
	
						<span v-html="item.icon"></span>
	
						<span> {{ item.title }} </span>
	
					</a>
	
				</li>
	
			</ul>	
			
	
			<ul v-if="loggedinUser.is_admin"
			    v-for="adminlinks in forAdmin">
	
				<li :class="{ active: adminlinks.active }">
	
					<a :href="adminlinks.link"
					   @click="changeActive(adminlinks.title)">
	
						<span v-html="adminlinks.icon"></span>
	
						<span> {{ adminlinks.title }} </span>
	
					</a>
	
				</li>
	
			</ul>
	
		</nav>
	
	</div>
</template>


		<style lang="sass">



			.side-list ul li a span i {
				color: #FDFAFA !important;
			}

		</style>