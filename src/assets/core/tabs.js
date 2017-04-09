

export default {

	template: `

		<div>

            <div class="container" id="exTab3" style="padding: 0px; margin: 0px;">
                <ul class="nav nav-pills">
                    <li v-for="tab in tabs" :class="{ 'is-active': tab.isActive }">
                        <a :href="tab.href" @click="selectTab(tab)">{{ tab.name }}</a>
                    </li>
                </ul>

                <div class="tab-content clearfix" data-toggle="tab">
                	<slot></slot>
            	</div>
            </div>

            

        </div>

	`,


	data() {

		return {

			tabs: []
		};
	},

	created() {
		this.tabs = this.$children;
	},


	methods: {

		selectTab(selectTab) {
			this.tabs.forEach(tab => {
				tab.isActive = ( tab.href == selectTab.href );
			});
		}
	}
}

// <div class="tab-content clearfix">                                       

//                                         <div class="tab-pane active" id="overview">

//                                             <h3>UCS-OVERVIEW</h3>
//                                         </div>
//                                     </div>