
<script>
	export default {

		props: { modalname: {required: true, default: 'default-modal'}},

		data() {
			return {

			}
		},


		mounted() {
			this.$nextTick(function(){

				$(`#${this.modalname}`).modal('show'); 
				$(`#${this.modalname}`).modal({
					backdrop: 'static',
					keyboard: true
				})

				$(`#${this.modalname}`).on("hidden.bs.modal", function () {

					eventBroadcaster.$emit('closeFaultsDetails')
				});

			});
		},

		methods: {

		},

		computed() {

		}

	}
</script>

<template>
	
	<div>

		<div class="modal fade" :id="modalname" tabindex="-1" role="dialog" data-backdrop="static" 
		data-keyboard="false">

		<div class="modal-dialog">

			<div class="modal-content">

				<div class="modal-header">
					<button @click="$emit('closeFaultsDetails')" type="button " class="close" data-dismiss="modal" aria-hidden="true">&times;</button>

					<h4 class="modal-title"> 

						<slot name='title'></slot>

					</h4>

				</div>

				<div class="modal-body">

					<slot name='body'></slot>

				</div>


				<div class="modal-footer">

					<slot name='footer'></slot>
					<button @click="$emit('closeFaultsDetails')" type="button" class="btn btn-xs btn-default" data-dismiss="modal">Close</button>
				</div>

			</div>
		</div>
	</div>

</div>
</template>

<style>
	
</style>
