<script>

	export default {
		
		props: ['user'],		

		data () {

			return {	
				loggedinUser: {},		

			}
		},

		mounted () {

			this.$nextTick( function() {

				
				this.getUser()

			})

			

		},


		methods: {		

			getUser () {

				axios.get(`/api/user/${this.user}`).
				then(response => {		
					console.log(response.data)			
					this.loggedinUser = response.data
				})
			}

		},


		computed: {
			
		}
		
	}
	
</script> 


<template>

	

	<div class="header">

		<div class="logo" style="margin-left: 20px;">
			<i class=""></i>
			<span></span>
		</div>

		<a href="#" class="nav-trigger"><span></span></a>




		<div class="navmenu" id="myNavbar">

			<ul class="" style="margin-top: 10px;">

				<!-- <li v-if=" loggedinUser.length <= 0"><a href="#"><span class="glyphicon glyphicon-log-in"></span> Login</a></li> -->

				<li>

					<li v-if=" loggedinUser >= 1 "><a href="/logout"><span class="glyphicon glyphicon-log-in"></span> Logout</a></li>					

					<!-- <li class="active"><a href="#">Home</a>  -->

					</li>

					<li>

						<li class="dropdown hidden-xs" >

							<!-- Menu Toggle Button -->
							<a href="#" class="dropdown-toggle" data-toggle="dropdown">

								<img style="border: 2px solid lightgrey; padding: 2px; margin-right: 7px; height: 35px; width: 35px; border-radius: 50%; background: #E9E8E8;" src="/static/img/prof.jpg" class="user-image" alt="User Image"/>

								<span class="hidden-xs">{{ loggedinUser.first_name }} {{ loggedinUser.last_name }}</span>

							</a>

							<ul class="dropdown-menu" style="border-top-right-radius: 0;
							border-top-left-radius: 0;
							padding: 1px 0 0 0;
							border-top-width: 0;
							width: 280px;
							position: absolute; 
							right: 20px;
							margin: 4px;
							margin-top: 21px;                   
							left: auto;">


							<li class="user-header" style="height: 175px; padding: 10px; text-align: center;">
								<center>
									<img src="/static/img/prof.jpg" class="img-circle" alt="User Image"/ style="z-index: 5;
									height: 90px;
									width: 90px;
									border: 3px solid;
									border-color: transparent;
									border-color: rgba(255, 255, 255, 0.2);">
								</center>



								<p style="z-index: 5;
								color: #fff;
								color: rgba(255, 255, 255, 0.8);
								font-size: 17px;
								margin-top: 10px;">

								{{ loggedinUser.first_name }} {{ loggedinUser.last_name }}              
							</p>

						</li>


						<li class="user-body" style="border-bottom-right-radius: 4px;
						border-bottom-left-radius: 4px;">


                </li>


                <li class="user-footer" style="display: list-item;
                text-align: -webkit-match-parent; ">

                <div class="pull-left">
                	<a href="/user/1/profile" class="btn btn-default btn-flat">Profile</a>
                </div>

                <div class="pull-right" v-if=" loggedinUser.length > 0 ">

                	<a href="/" class="btn btn-default btn-flat" onclick="event.preventDefault(); document.getElementById('logout-form').submit();">
                		Logout
                	</a>

                </div>

                <form id="logout-form" action="/" method="POST" style="display: none;">

                </form>

            </li>
        </ul>
    </li>

</li>

<li class="hidden-xs">&nbsp;</li>

</ul>

</div>


</div>

</template>


<style lang="sass">



	.side-list ul li a span i {
		color: #FDFAFA !important;
	}

</style>