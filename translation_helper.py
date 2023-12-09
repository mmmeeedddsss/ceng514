from gpt import OpenAIWrapper


class TranslationHelper:
    REQUEST_CHUNK_SIZE = 20

    @staticmethod
    def _chunks(lst, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    @staticmethod
    def translate_prompts_to_turkish(dataset):
        prompts = [d['question'] for d in dataset]
        chunks_of_prompts = list(TranslationHelper._chunks(prompts, TranslationHelper.REQUEST_CHUNK_SIZE))

        dataset = dataset.copy()
        for chunk_no, chunk in enumerate(chunks_of_prompts):
            translated_prompts = OpenAIWrapper.translate_to_turkish(chunk).split('\n')

            for prompt_no, translated_prompt in enumerate(translated_prompts):
                first_dot = translated_prompt.find('.')

                prompt_index_in_dataset = chunk_no * TranslationHelper.REQUEST_CHUNK_SIZE + prompt_no
                dataset[prompt_index_in_dataset]['question'] = translated_prompt[first_dot+1:].strip()

        return dataset
